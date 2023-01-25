# Databricks notebook source
dbutils.widgets.text("ProcessMonth", "201812", "Process Month (yyyymm)")
dbutils.widgets.dropdown("env", "dev", ["dev", "test", "qa", "prod"])

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql import types as T

# COMMAND ----------

class WriteFHVTaxi:
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
            .where((F.col("PUlocationID").isNotNull()) & (F.col("DOlocationID").isNotNull()))
            .where((F.col("Pickup_DateTime") >= "2018-12-01") & (F.col("DropOff_datetime") < "2019-01-01"))

            .withColumn("TripType", F.when(F.col("SR_Flag") == 1, "Shared").otherwise("Solo"))
            .withColumn("TripDuration", ((F.unix_timestamp(F.col("DropOff_datetime")) - F.unix_timestamp(F.col("Pickup_DateTime")))/60).cast("integer"))

            .drop(F.col("SR_Flag"))
            .drop(F.col("Dispatching_base_num"))

            .withColumnRenamed("Pickup_DateTime", "PickupTime")
            .withColumnRenamed("DropOff_datetime", "DropTime")
            .withColumnRenamed("Dispatching_base_number", "BaseLicenceNumber")
          
            .join
            (
                F.broadcast(spark.sql("select * from TaxiTrips.DimFHVBases")),
                "BaseLicenceNumber",
                "left"
            )
        )
    
    def WriteToDeltaTable(self) -> None: 
        
        (
        self.GetProcessedData
        .write
        .mode("overwrite")
        .format("delta")
        .option("path", f'{self.targetPath}/AllVersions')
        .saveAsTable("TaxiTrips.FactFHVTaxi")
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

WriteFHVTaxiObj = WriteFHVTaxi(
    schema = schema_FHVtaxi,
    options = {"header":"true"},
    sourcePath = f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/Raw/FHVTaxiTripData_{dbutils.widgets.get("ProcessMonth")}_01.csv',
    targetPath = f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/Processed/Facts/FHVTaxi'
)

WriteFHVTaxiObj.WriteToDeltaTable()
WriteFHVTaxiObj.WriteToDataLake()

# COMMAND ----------

dbutils.notebook.exit("Success")
