# Databricks notebook source
# %sql
# drop table customerdata.customersbronze

# COMMAND ----------

# %sql
# drop table customerdata.customerssilver

# COMMAND ----------

dbutils.widgets.dropdown("env", "dev", ["dev", "test", "qa", "prod"])

# COMMAND ----------

import dlt
from pyspark.sql import functions as F 
from pyspark.sql import types as T

# COMMAND ----------

# MAGIC %md
# MAGIC #### Autoloader in Databricks using cloudFiles as the source
# MAGIC - Incrementally read the new files in the Bronze layer 
# MAGIC - Add the current timestamp and append it in the Bronze layer 

# COMMAND ----------

@dlt.table
def customersBronze():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.schemaLocation", f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/AutoLoaderStoragePath/')
        .load(f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/AutoLoader/')
  )

@dlt.table

def customersSilver():
    return (
        dlt.read_stream("customersBronze")
        .withColumn("ProcessedTimestamp", F.current_timestamp())
  )

# COMMAND ----------

# MAGIC %md
# MAGIC #### Read the silver layer for confirmation

# COMMAND ----------

display(
    spark.sql("select * from customerdata.customersbronze")
    .count()
)

# COMMAND ----------

display(
    spark.sql("select * from customerdata.customerssilver")
    .count()
)
