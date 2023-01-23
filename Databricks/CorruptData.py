# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql import types as T

# COMMAND ----------

# MAGIC %md
# MAGIC ### Corrput data
# MAGIC - **PERMISSIVE -** when it meets a corrupted record, puts the malformed string into a field configured by columnNameOfCorruptRecord, and sets other fields to null. To keep corrupt records, the user can set a string type field named columnNameOfCorruptRecord in an user-defined schema. If a schema does not have the field, it drops corrupt records during parsing. When inferring a schema, it implicitly adds a columnNameOfCorruptRecord field in an output schema.
# MAGIC 
# MAGIC - **DROPMALFORMED -** ignores the whole corrupted records.
# MAGIC 
# MAGIC - **FAILFAST -** throws an exception when it meets corrupted records.

# COMMAND ----------

df_RateCodeSchema = T.StructType(
    [
        T.StructField("RateCode", T.StringType(), True), 
        T.StructField("RateCodeID", T.IntegerType(), True), 
        T.StructField("_corrupt_record", T.StringType(), True)
    ]
)

# COMMAND ----------

display(
    spark
    .read
    .schema(df_RateCodeSchema)
    .format("json").load(f'/mnt/sadb01dev/commonfiles-{dbutils.widgets.get("env")}/Raw/RateCodes.json')
)

# COMMAND ----------

display(
    spark
    .read
    .option("mode", "DropMalformed")
    .format("json").load(f'/mnt/sadb01dev/commonfiles-{dbutils.widgets.get("env")}/Raw/RateCodes.json')
)

# COMMAND ----------

display(
    spark
    .read
    .option("mode", "FailFast")
    .format("json").load(f'/mnt/sadb01dev/commonfiles-{dbutils.widgets.get("env")}/Raw/RateCodes.json')
)

# COMMAND ----------

display(
    spark
    .read
    .option("BadRecordsPath", f'/mnt/sadb01dev/commonfiles-{dbutils.widgets.get("env")}')
    .format("json").load(f'/mnt/sadb01dev/commonfiles-{dbutils.widgets.get("env")}/Raw/RateCodes.json')
)

# COMMAND ----------

# MAGIC %md 
# MAGIC #### CSV files
# MAGIC The above behaviours would be different for the Permissive mode. In that case the missing values will be recorded as *null*. We can choose to either remove, or fail the execution, similar to json files. 
