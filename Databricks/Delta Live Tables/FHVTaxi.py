# Databricks notebook source
dbutils.widgets.text("ProcessMonth", "201812", "Process Month (yyyymm)")
dbutils.widgets.dropdown("env", "dev", ["dev", "test", "qa", "prod"])

# COMMAND ----------

import dlt
from pyspark.sql import functions as F 
from pyspark.sql import types as T

# COMMAND ----------

schema_FHVtaxi = T.StructType(
    [
        T.StructField("Pickup_DateTime", T.TimestampType(), True), 
        T.StructField("DropOff_datetime", T.TimestampType(), True),
        T.StructField("PUlocationID", T.IntegerType(), True),
        T.StructField("DOlocationID", T.IntegerType(), True),
        T.StructField("SR_Flag", T.IntegerType(), True),
        T.StructField("Dispatching_base_number", T.StringType(), True),
        T.StructField("Dispatching_base_num", T.StringType(), True)
    ]
)

# COMMAND ----------

@dlt.view(
  comment="Raw FHV Taxi Data"
)

@dlt.expect_all_or_drop(
    {
    "Valid_DateTime": "Pickup_DateTime >= '2018-12-01' AND DropOff_datetime < '2019-01-01'",
    "Complete_LocationID": "PULocationID IS NOT NULL AND DOLocationID IS NOT NULL"
    }
)

def RawFHVTaxi():
    
    return (
        spark
        .read
        .options(**{"header":"true"})
        .schema(schema_FHVtaxi)
        .format("csv")
        .load(f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/Raw/FHVTaxiTripData_{dbutils.widgets.get("ProcessMonth")}_01.csv')
    )

@dlt.table(
  comment="Processed FHV Taxi Data"
)

def ProcessedFHVTaxi():
    
    return (
        dlt.read("RawFHVTaxi")

        .withColumn("TripType", F.when(F.col("SR_Flag") == 1, "Shared").otherwise("Solo"))
        .withColumn("TripDuration", ((F.unix_timestamp(F.col("DropOff_datetime")) - F.unix_timestamp(F.col("Pickup_DateTime")))/60).cast("integer"))

        .drop(F.col("SR_Flag"))
        .drop(F.col("Dispatching_base_num"))

        .withColumnRenamed("Pickup_DateTime", "PickupTime")
        .withColumnRenamed("DropOff_datetime", "DropTime")
        .withColumnRenamed("Dispatching_base_number", "BaseLicenceNumber")
        
        .join
            (
                F.broadcast(spark.sql("select * from live.ProcessedFHVBases")),
                "BaseLicenceNumber",
                "left"
            )
  )
