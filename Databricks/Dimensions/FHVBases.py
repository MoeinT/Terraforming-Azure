# Databricks notebook source
dbutils.widgets.dropdown("env", "dev", ["dev", "test", "qa", "prod"])

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql import types as T

# COMMAND ----------

class WriteFHVBases:
    def __init__(self, options, targetPath: str, sourcePath: str, sourceFormat = "json") -> None:
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
            .format(self.sourceFormat)
            .load(self.sourcePath)
        )
    
    @property
    def GetProcessedData(self): 
        
        return (
            self.ReadFromSource
            .select(
            F.col("Address.Building").alias("AddressBuilding"),
            F.col("Address.City").alias("AddressCity"),
            F.col("Address.Postcode").alias("AddressPostcode"),
            F.col("Address.State").alias("AddressState"),
            F.col("Address.Street").alias("AddressStreet"),

            F.col("License Number").alias("BaseLicenceNumber"),
            F.col("Type of Base").alias("BaseType")
            )
        )
    
    def WriteToDeltaTable(self) -> None: 
        
        (
        self.GetProcessedData
        .write
        .mode("overwrite")
        .format("delta")
        .option("path", f'{self.targetPath}/AllVersions')
        .saveAsTable("TaxiTrips.DimFHVBases")
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

WriteFHVBasesObj = WriteFHVBases(
    options = {"header":"true", "InferSchema": "true", "multiline": "true"},
    sourcePath = f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/Raw/FhvBases.json',
    targetPath = f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/Processed/Dims/FHVBases'
)

WriteFHVBasesObj.WriteToDeltaTable()
WriteFHVBasesObj.WriteToDataLake()

# COMMAND ----------

dbutils.notebook.exit("Success")
