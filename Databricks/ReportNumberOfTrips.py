# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql import types as T

# COMMAND ----------

# MAGIC %md
# MAGIC ### Reports
# MAGIC #### Number of rides grouped by taxi type and borough

# COMMAND ----------

(
    spark
    .read
    .option("header", "true")
    .option("InferSchema", "true")
    .format("csv").load(f'/mnt/sadb01dev/commonfiles-{dbutils.widgets.get("env")}/Raw/TaxiZones.csv')
    
    .withColumnRenamed("service_zone", "ServiceZone")
    
    .write
    .mode("overwrite")
    .format("delta")
    .saveAsTable("TaxiTrips.DimTaxiZones")
)

# COMMAND ----------

df_allTaxis = (
    spark.sql("select PickupTime, DropTime, PULocationID, DOLocationID, TripDuration, 'Yellow' as TaxiType from TaxiTrips.FactYellowTaxi")
    .union(
        spark.sql("select PickupTime, DropTime, PULocationID, DOLocationID, TripDuration, 'Green' as TaxiType from TaxiTrips.FactGreenTaxi")
    )
    .union(
        spark.sql("select PickupTime, DropTime, PULocationID, DOLocationID, TripDuration, BaseType as TaxiType from TaxiTrips.FactFHVTaxi")
    )
)

df_TaxiZones = (
    spark.sql("select * from TaxiTrips.DimTaxiZones")
)

(
    df_allTaxis
    .where(F.col("TaxiType").isNotNull())
    .join
    (
        df_TaxiZones
        .where(F.col("Borough").isNotNull()), 
        df_allTaxis.PULocationID == df_TaxiZones.LocationID, 
        "left"
    )
    
    .groupBy(["Borough", "TaxiType"])
    .count()
    
    .withColumnRenamed("count", "NumberOfTrips")
    .orderBy(F.col("NumberOfTrips").desc())
    
    .write
    .mode("overwrite")
    .format("delta")
    .saveAsTable("TaxiTrips.ReportNumberOfTrips")
)
