# Databricks notebook source
dbutils.widgets.dropdown("env", "dev", ["dev", "test", "qa", "prod"])

# COMMAND ----------

from pyspark.sql import functions as F 
from pyspark.sql import types as T

# COMMAND ----------

df_insurance = (
            spark
            .read
            .options(**{"header":"true"})
            .format("csv")
            .load(f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/customerData/insurance.csv')
            
            .repartition(4)
        )

# COMMAND ----------

df_insurance.rdd.getNumPartitions()

# COMMAND ----------

df_insurance.show()

# COMMAND ----------

(
    df_insurance
    .count()
)

# COMMAND ----------

# MAGIC %md
# MAGIC - **Notice that here 3 partitions where involved in reading 1000 rows of the dataset, but they were not all returned into one partition as the final stage; here we didn't have a shuffle write**

# COMMAND ----------

(
    df_insurance
    .select(F.col("sex"), F.col("smoker"), F.col("age"))
  .show(5)
)

# COMMAND ----------

# MAGIC %md
# MAGIC - **Notice that here the 4 partitions were involved to select the "sex" column in parallel. Once that was finished, all the 4 partitions were return back to the driver node into a bigger partition to compute the distinct values. See there's a final stage**

# COMMAND ----------

display(
    df_insurance
    .select(F.col("sex"))
    .distinct()
)

# COMMAND ----------

display(
    df_insurance
    .orderBy(F.col("bmi").desc())
)

# COMMAND ----------

display(
    df_insurance
    .select(F.col("sex"), F.col("bmi"), F.col("children"))
    .where(F.col("region") == "southwest")
    .orderBy(F.col("bmi").desc())
)

# COMMAND ----------

display(
    df_insurance
    .groupBy(F.col("sex"))
    .count()
)

# COMMAND ----------

display(
    df_insurance
    .groupBy(F.col("smoker"))
    .agg({"bmi": "avg", "sex": "count", "charges": "avg"})
    .withColumnRenamed("avg(bmi)", "avg_bmi")
    .withColumnRenamed("count(sex)", "count")
    .withColumnRenamed("avg(charges)","avg_charges")
)

# COMMAND ----------


