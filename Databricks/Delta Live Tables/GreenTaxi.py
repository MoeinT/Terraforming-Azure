# Databricks notebook source
dbutils.widgets.text("ProcessMonth", "201812", "Process Month (yyyymm)")
dbutils.widgets.dropdown("env", "dev", ["dev", "test", "qa", "prod"])

# COMMAND ----------

import dlt
from pyspark.sql import functions as F 
from pyspark.sql import types as T

# COMMAND ----------

GreenTaxiSchema = T.StructType(
    [
        T.StructField("VendorID", T.IntegerType(), True), 
        T.StructField("lpep_pickup_datetime", T.TimestampType(), True), 
        T.StructField("lpep_dropoff_datetime", T.TimestampType(), True), 
        T.StructField("store_and_fwd_flag", T.StringType(), True),
        T.StructField("RatecodeID", T.IntegerType(), True),
        T.StructField("PULocationID", T.IntegerType(), True),
        T.StructField("DOLocationID", T.IntegerType(), True),
        T.StructField("passenger_count", T.IntegerType(), True),
        T.StructField("trip_distance", T.DoubleType(), True),
        T.StructField("fare_amount", T.DoubleType(), True),
        T.StructField("extra", T.DoubleType(), True),
        T.StructField("mta_tax", T.DoubleType(), True),
        T.StructField("tip_amount", T.DoubleType(), True),
        T.StructField("tolls_amount", T.DoubleType(), True),
        T.StructField("ehail_fee", T.StringType(), True),
        T.StructField("improvement_surcharge", T.DoubleType(), True),
        T.StructField("total_amount", T.DoubleType(), True),
        T.StructField("payment_type", T.IntegerType(), True),
        T.StructField("trip_type", T.IntegerType(), True)
    ]
    )

# COMMAND ----------

@dlt.view(
  comment="Raw Yellow Taxi Trip Data"
)

@dlt.expect_all_or_drop(
    {
    "valid_TripDistance": "trip_distance > 0.0", 
    "valid_PassengerCount": "passenger_count > 0 AND passenger_count < 5",
    "Valid_DateTime": "lpep_pickup_datetime >= '2018-12-01' AND lpep_dropoff_datetime < '2019-01-01'",
    "Complete_LocationID": "PULocationID IS NOT NULL AND DOLocationID IS NOT NULL"
    }
)

def RawGreenTaxi():
    
    return (
        spark
        .read
        .options(**{"header":"true", "delimiter": "\t"})
        .schema(GreenTaxiSchema)
        .format("csv")
        .load(f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/Raw/GreenTaxiTripData_{dbutils.widgets.get("ProcessMonth")}.csv')
    )

@dlt.table(
  comment="Processed Yellow Taxi Trip Data."
)

def ProcessedGreenTaxi():
    
    return (
        dlt.read("RawGreenTaxi")
        .where(F.col("trip_distance") > 0.0)
        .where((F.col("passenger_count") > 0) & (F.col("passenger_count") < 5))
        .where((F.col("PULocationID").isNotNull()) & (F.col("DOLocationID").isNotNull()))
        .where((F.col("lpep_pickup_datetime") >= "2018-12-01") & (F.col("lpep_dropoff_datetime") < "2019-01-01"))
        
        .withColumn("TripDuration", ((F.unix_timestamp(F.col("lpep_dropoff_datetime")) -  F.unix_timestamp(F.col("lpep_pickup_datetime")))/60).cast("integer") )
        .withColumnRenamed("lpep_pickup_datetime", "PickupTime")
        .withColumnRenamed("lpep_dropoff_datetime", "DropTime")
        .withColumnRenamed("passenger_count", "PassengerCount")
        .withColumnRenamed("trip_distance", "TripDistance")
        .withColumnRenamed("trip_type", "TripType")

  )
