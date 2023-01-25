# Databricks notebook source
dbutils.widgets.text("ProcessMonth", "201812", "Process Month (yyyymm)")
dbutils.widgets.dropdown("env", "dev", ["dev", "test", "qa", "prod"])

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql import types as T

# COMMAND ----------

class WriteGreenTaxi:
    def __init__(self, schema: T.StructType, options, targetPath: str, sourcePath: str, sourceFormat = "csv") -> None:
            self.schema = schema
            self.sourcePath = sourcePath
            self.sourceFormat = sourceFormat
            self.targetPath = targetPath
            self.options = options
    
    @property
    def ReadFromSource(self):
        
        return (
            spark
            .read
            .options(**self.options)
            .schema(self.schema)
            .format(self.sourceFormat)
            .load(self.sourcePath)
        )
    
    @property
    def GetProcessedData(self): 
        
        return (
            self.ReadFromSource
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
    
    def WriteToDeltaTable(self) -> None: 
        
        (
        self.GetProcessedData
        .write
        .mode("overwrite")
        .format("delta")
        .option("path", f'{self.targetPath}/AllVersions')
        .saveAsTable("TaxiTrips.FactGreenTaxi")
        )
    
    def WriteToDataLake(self) -> None: 
        
        (
        self.GetProcessedData
        .write
        .format("parquet")
        .mode("overwrite")
        .save(f'{self.targetPath}/MostUpdatedVersion')
        )


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

WriteGreenTaxiObj = WriteGreenTaxi(
    schema = GreenTaxiSchema,
    options = {"header":"true", "delimiter": "\t"},
    sourcePath = f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/Raw/GreenTaxiTripData_{dbutils.widgets.get("ProcessMonth")}.csv',
    targetPath = f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/Processed/Facts/GreenTaxi'
)

WriteGreenTaxiObj.WriteToDeltaTable()
WriteGreenTaxiObj.WriteToDataLake()

# COMMAND ----------

dbutils.notebook.exit("Success")
