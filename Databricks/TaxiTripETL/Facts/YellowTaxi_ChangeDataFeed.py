# Databricks notebook source
dbutils.widgets.text("ProcessMonth", "201812", "Process Month (yyyymm)")
dbutils.widgets.dropdown("env", "dev", ["dev", "test", "qa", "prod"])

# COMMAND ----------

from pyspark.sql import functions as F 
from pyspark.sql import types as T

# COMMAND ----------

class WriteYellowTaxi:
    def __init__(self, schema: T.StructType, options, targetPath: str, sourcePath: str, sourceFormat = "csv") -> None:
            self.schema = schema
            self.sourcePath = sourcePath
            self.sourceFormat = sourceFormat
            self.targetPath = targetPath
            self.options = options
    
    def ReadFromSource(self):
        
        return (
            spark
            .read
            .options(**self.options)
            .schema(self.schema)
            .format(self.sourceFormat)
            .load(self.sourcePath)
            
            .write
            .mode("overwrite")
            .format("delta")
            .option("path", f'{self.targetPath}/Bronze')
            .saveAsTable("TaxiTrips.YellowTaxiBronze")
        )
    
    
    def StoreProcessedData(self):
        
        (
            spark.read.format("delta")
            .option("readChangeFeed", "true")
            .option("startingVersion", 1)
            .table("TaxiTrips.YellowTaxiBronze")
            
            .where(F.col("trip_distance") > 0.0)
            .where((F.col("passenger_count") > 0) & (F.col("passenger_count") < 5))
            .where((F.col("PULocationID").isNotNull()) & (F.col("DOLocationID").isNotNull()))
            .where((F.col("tpep_pickup_datetime") >= "2018-12-01") & (F.col("tpep_dropoff_datetime") < "2019-01-01"))

            .withColumn("TripDuration", ((F.unix_timestamp(F.col("tpep_dropoff_datetime")) - F.unix_timestamp(F.col("tpep_pickup_datetime")))/60).cast("integer") )

            .withColumnRenamed("tpep_pickup_datetime", "PickupTime")
            .withColumnRenamed("tpep_dropoff_datetime", "DropTime")
            .withColumnRenamed("passenger_count", "PassengerCount")
            .withColumnRenamed("trip_distance", "TripDistance")
            .withColumnRenamed("trip_type", "TripType")
            .drop_duplicates()
            
            .write
            .mode("overwrite")
            .format("delta")
            .saveAsTable("TaxiTrips.YellowTaxiSilverChange")
        )
        
        dl_sourceYellowTaxi = DeltaTable.forPath(spark, "TaxiTrips.YellowTaxiSilverChange")
        dl_targetYellowTaxi = DeltaTable.forPath(spark, "TaxiTrips.YellowTaxiSilver")
        
        (
            dl_targetYellowTaxi.alias('target')
            .merge(
                df_YellowTaxiProcessed.alias('source'),
                """
                target.VendorID = source.VendorID and 
                target.PickupTime = source.PickupTime and 
                target.DropTime = source.DropTime and 
                target.PassengerCount = source.PassengerCount
                """
            )
            .whenNotMatchedInsert(set = {"target.VendorID": "source.VendorID"})
            .whenMatchedUpdate(set = {"target.VendorID": "source.VendorID"})
            .execute()
        )
        

# COMMAND ----------

YellowTaxiSchema = T.StructType(
    [
        T.StructField("VendorID", T.IntegerType(), True), 
        T.StructField("tpep_pickup_datetime", T.TimestampType(), True), 
        T.StructField("tpep_dropoff_datetime", T.TimestampType(), True), 
        T.StructField("passenger_count", T.IntegerType(), True),
        T.StructField("trip_distance", T.DoubleType(), True),
        T.StructField("RatecodeID", T.IntegerType(), True),
        T.StructField("store_and_fwd_flag", T.StringType(), True),
        T.StructField("PULocationID", T.IntegerType(), True),
        T.StructField("DOLocationID", T.IntegerType(), True),
        T.StructField("payment_type", T.IntegerType(), True),
        T.StructField("fare_amount", T.DoubleType(), True),
        T.StructField("extra", T.DoubleType(), True),
        T.StructField("mta_tax", T.DoubleType(), True),
        T.StructField("tip_amount", T.DoubleType(), True),
        T.StructField("tolls_amount", T.DoubleType(), True),
        T.StructField("improvement_surcharge", T.DoubleType(), True),
        T.StructField("total_amount", T.DoubleType(), True)
    ]
    )

# COMMAND ----------

WriteYellowTaxiObj = WriteYellowTaxi(
    schema = YellowTaxiSchema,
    options = {"header":"true"},
    sourcePath = f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/Raw/YellowTaxiTripData_{dbutils.widgets.get("ProcessMonth")}.csv',
    targetPath = f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/Processed/Facts/YellowTaxi'
)


WriteYellowTaxiObj.ReadFromSource()
WriteYellowTaxiObj.StoreProcessedData()


# COMMAND ----------

dbutils.notebook.exit("Success")

# COMMAND ----------

# %sql
# ALTER TABLE TaxiTrips.YellowTaxiBronze SET TBLPROPERTIES (delta.enableChangeDataFeed = true)

# COMMAND ----------

# %sql
# INSERT INTO TaxiTrips.YellowTaxiBronze 
# (VendorID, tpep_pickup_datetime, tpep_dropoff_datetime,passenger_count,trip_distance, RatecodeID, store_and_fwd_flag, PULocationID, DOLocationID, payment_type, fare_amount, extra, mta_tax, tip_amount, tolls_amount, improvement_surcharge, total_amount)
# VALUES (10, '2018-12-01T00:40:56.000+0000', '2018-12-01T00:41:02.000+0000', 3, 0, 5, 'N', 168, 168, 1, 65, 0, 0.5, 60, 0, 0.3, 125.8);

# COMMAND ----------

# %sql
# DESCRIBE HISTORY TaxiTrips.YellowTaxiBronze

# COMMAND ----------

# %sql
# SELECT * FROM table_changes('TaxiTrips.YellowTaxiBronze', 0)
