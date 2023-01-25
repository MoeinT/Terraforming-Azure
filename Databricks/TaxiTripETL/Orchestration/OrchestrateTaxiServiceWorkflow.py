# Databricks notebook source
dbutils.widgets.text("ProcessMonth", "201812", "Process Month (yyyymm)")
dbutils.widgets.dropdown("env", "dev", ["dev", "test", "qa", "prod"])

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql import types as T

# COMMAND ----------

status = (
    dbutils
    .notebook
    .run(
        "../Facts/YellowTaxi",
        300
    )
)

if status == "Success":
    print("Yellow Taxi Facts has been processed successfully.")
else:
    print("Error in processing Yellow Taxi Fact.")

# COMMAND ----------


