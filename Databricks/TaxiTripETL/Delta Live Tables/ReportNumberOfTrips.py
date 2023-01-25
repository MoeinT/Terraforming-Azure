# Databricks notebook source
dbutils.widgets.text("ProcessMonth", "201812", "Process Month (yyyymm)")
dbutils.widgets.dropdown("env", "dev", ["dev", "test", "qa", "prod"])

# COMMAND ----------

# MAGIC %md
# MAGIC ### Reports
# MAGIC #### Number of rides grouped by taxi type and borough

# COMMAND ----------

import dlt
from pyspark.sql import functions as F 
from pyspark.sql import types as T

# COMMAND ----------

@dlt.view(
  comment="Taxi Zones Data"
)
def TaxiZones():
    
    return (
        spark
        .read
        .option("header", "true")
        .option("InferSchema", "true")
        .format("csv").load(f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/Raw/TaxiZones.csv')
    )

@dlt.view(
  comment="Processed FHV Bases"
)

def MergeAllTaxis():
    
    return (    
        spark.sql("select PickupTime, DropTime, PULocationID, DOLocationID, TripDuration, 'Yellow' as TaxiType from live.ProcessedYellowTaxi")
        .union(
            spark.sql("select PickupTime, DropTime, PULocationID, DOLocationID, TripDuration, 'Green' as TaxiType from live.ProcessedGreenTaxi")
        )
        .union(
            spark.sql("select PickupTime, DropTime, PULocationID, DOLocationID, TripDuration, BaseType as TaxiType from live.ProcessedFHVTaxi")
        )
  )

@dlt.table(
  comment="Final Report"
)

def FinalReport():
    
    return (
        dlt.read("MergeAllTaxis")
        .where(F.col("TaxiType").isNotNull())
        .alias("MergeAllTaxis")
        
        .join
        (
            dlt.read("TaxiZones").alias("TaxiZones")
            .where(F.col("Borough").isNotNull()), 
            F.col("MergeAllTaxis.PULocationID") == F.col("TaxiZones.LocationID"),
            "left"
        )
        
        .groupBy(["Borough", "TaxiType"])
        .count()
        
        .withColumnRenamed("count", "NumberOfTrips")
        .orderBy(F.col("NumberOfTrips").desc())
  )
