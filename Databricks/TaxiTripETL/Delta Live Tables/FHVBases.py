# Databricks notebook source
dbutils.widgets.dropdown("env", "dev", ["dev", "test", "qa", "prod"])

# COMMAND ----------

import dlt
from pyspark.sql import functions as F 
from pyspark.sql import types as T

# COMMAND ----------

@dlt.view(
  comment="Raw FHV Bases"
)
def RawFHVBases():
    return (
        spark
        .read
        .options(**{"header":"true", "InferSchema": "true", "multiline": "true"})
        .format("json")
        .load(f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/Raw/FhvBases.json')
    )

@dlt.table(
  comment="Processed FHV Bases"
)

def ProcessedFHVBases():
    return (
        dlt.read("RawFHVBases")
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
