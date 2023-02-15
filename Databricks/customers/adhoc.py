# Databricks notebook source
dbutils.widgets.dropdown("env", "dev", ["dev", "test", "qa", "prod"])

# COMMAND ----------

from pyspark.sql import functions as F 
from pyspark.sql import types as T
import pandas as pd
from typing import *

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

# MAGIC %md
# MAGIC #### Load data

# COMMAND ----------

# MAGIC %sql
# MAGIC create database if not exists CustomerData

# COMMAND ----------

load_schema = T.StructType(
    [
        T.StructField("ID", T.IntegerType(), True), 
        T.StructField("Default", T.IntegerType(), True),
        T.StructField("Loan_type", T.StringType(), True),
        T.StructField("Gender", T.StringType(), True),
        T.StructField("Age", T.IntegerType(), True),
        T.StructField("Degree", T.StringType(), True),
        T.StructField("Income", T.IntegerType(), True),
        T.StructField("Credit_score", T.IntegerType(), True),
        T.StructField("Loan_length", T.IntegerType(), True),
        T.StructField("Signers", T.IntegerType(), True),
        T.StructField("Citizenship:", T.StringType(), True)
    ]
)

df_loanData = (
    spark
    .read
    .format("csv")
    .options(**{"header":"true"})
    .schema(load_schema)
    .load(f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/customerData/loan_data.csv')
    
    .repartition(4)
)

(
    df_loanData
    .write
    .mode("overwrite")
    .format("delta")
    .saveAsTable("CustomerData.Loans")
)

# COMMAND ----------

df_loanData.rdd.getNumPartitions()

# COMMAND ----------

display(
    spark.sql("""
    select Degree, avg(Income) as avg_income from CustomerData.Loans
    group by Degree
    having avg_income > 100000
    order by avg_income desc
    """)
)

# COMMAND ----------

display(
    spark.sql("""
    select Gender, avg(Income) from CustomerData.Loans
    group by Gender
    """)
)

# COMMAND ----------

# MAGIC %md 
# MAGIC #### Converting csv to json

# COMMAND ----------

df_SuperstoreData = (
    spark
    .read
    .format("csv")
    .options(**{"header": "true"})
    .load(f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/customerData/US Superstore data - Orders.csv')
    
    .withColumnRenamed("Row ID", "id")
)

df_SuperstoreData = (
    df_SuperstoreData
    .select([F.col(col).alias(col.replace(' ', '')) for col in df_SuperstoreData.columns])
)

# COMMAND ----------

display(
    df_SuperstoreData
)

# COMMAND ----------

(
    df_SuperstoreData
    .select([F.col(col).alias(col.replace(' ', '')) for col in df_SuperstoreData.columns])
    .write
    .mode("overwrite")
    .json(f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/customerData/SuperstoreJson')    
)


# COMMAND ----------

# MAGIC %md 
# MAGIC ### Loading to Cosmos DB

# COMMAND ----------

# Configure Catalog Api to be used
spark.conf.set("spark.sql.catalog.cosmosCatalog", "com.azure.cosmos.spark.CosmosCatalog")
spark.conf.set("spark.sql.catalog.cosmosCatalog.spark.cosmos.accountEndpoint", cosmosEndpoint)
spark.conf.set("spark.sql.catalog.cosmosCatalog.spark.cosmos.accountKey", cosmosMasterKey)

# COMMAND ----------

class ConnToCosmosDB:
    def __init__(self, container: str, database: str, cosmosMasterKey: str, cosmosEndpoint: str) -> None:
            self.container = container
            self.database = database
            self.cosmosMasterKey = cosmosMasterKey
            self.cosmosEndpoint = cosmosEndpoint
    
    @property
    def getConfig(self):
        return (
            {
                "spark.cosmos.accountEndpoint": self.cosmosEndpoint,
                "spark.cosmos.accountKey": self.cosmosMasterKey,
                "spark.cosmos.database": self.database, 
                "spark.cosmos.container": self.container,
                "spark.cosmos.read.inferSchema.enabled": "true"
            }
        )
    
    @property
    def getData(self):
        return (
            spark
            .read
            .format("cosmos.oltp")
            .options(**self.getConfig)
            .load()
        )
        

# COMMAND ----------

cosmosobj = ConnToCosmosDB(
    cosmosEndpoint = "https://testcosmos-dev.documents.azure.com:443/",
    cosmosMasterKey = "rPN73A2UqL9BWnGmqysslTlBZiywWQY2sgARmy22bgkFdLTKxSOJxJ2bl5nEwuFAKukSvNK8dIuZACDbMi2hTA==",
    database = "Families-dev",
    container = "superstore-container-dev"
)

display(
    cosmosobj.getData
    .count()
)

# COMMAND ----------

# cosmosEndpoint = "https://testcosmos-dev.documents.azure.com:443/"
# cosmosMasterKey = "rPN73A2UqL9BWnGmqysslTlBZiywWQY2sgARmy22bgkFdLTKxSOJxJ2bl5nEwuFAKukSvNK8dIuZACDbMi2hTA=="
# atabase = "Families-dev"
# container = "superstore-container-dev"

# cfg = {
#     "spark.cosmos.accountEndpoint": cosmosEndpoint,
#     "spark.cosmos.accountKey": cosmosMasterKey,
#     "spark.cosmos.database": database,
#     "spark.cosmos.container": container,
#     "spark.cosmos.read.inferSchema.enabled": "true"
# }# cosmosEndpoint = "https://testcosmos-dev.documents.azure.com:443/"
# cosmosMasterKey = "rPN73A2UqL9BWnGmqysslTlBZiywWQY2sgARmy22bgkFdLTKxSOJxJ2bl5nEwuFAKukSvNK8dIuZACDbMi2hTA=="
# atabase = "Families-dev"
# container = "superstore-container-dev"

# cfg = {
#     "spark.cosmos.accountEndpoint": cosmosEndpoint,
#     "spark.cosmos.accountKey": cosmosMasterKey,
#     "spark.cosmos.database": database,
#     "spark.cosmos.container": container,
#     "spark.cosmos.read.inferSchema.enabled": "true"
# }

# COMMAND ----------

# (
#     df_SuperstoreData
#     .write
#     .format("cosmos.oltp")
#     .options(**cfg)
#     .mode("APPEND")
#     .save()
# )

# COMMAND ----------

df_superstore = (
    spark.sql("select * from CustomerData.superstore")
)

display(
    df_superstore
)

# COMMAND ----------

# MAGIC %md
# MAGIC #### How to use Pandas UDFs 

# COMMAND ----------

def year(date: pd.Series) -> pd.Series:
    return (pd.to_datetime(date).dt.year)

# COMMAND ----------

year_pandas_udf = F.pandas_udf(year, T.IntegerType())

display(
    df_superstore
    .withColumn("year", year_pandas_udf(F.col("OrderDate")))
)

# COMMAND ----------

# MAGIC %md 
# MAGIC #### Exploring repartitioning

# COMMAND ----------

from pyspark.sql import functions as F 
from pyspark.sql import types as T

load_schema = T.StructType(
    [
        T.StructField("ID", T.IntegerType(), True), 
        T.StructField("Default", T.IntegerType(), True),
        T.StructField("Loan_type", T.StringType(), True),
        T.StructField("Gender", T.StringType(), True),
        T.StructField("Age", T.IntegerType(), True),
        T.StructField("Degree", T.StringType(), True),
        T.StructField("Income", T.IntegerType(), True),
        T.StructField("Credit_score", T.IntegerType(), True),
        T.StructField("Loan_length", T.IntegerType(), True),
        T.StructField("Signers", T.IntegerType(), True),
        T.StructField("Citizenship:", T.StringType(), True)
    ]
)

df_loanData = (
    spark
    .read
    .format("csv")
    .options(**{"header":"true"})
    .schema(load_schema)
    .load(f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/customerData/loan_data.csv')
    
    .repartition(4)
)

print(df_loanData.rdd.getNumPartitions())

# COMMAND ----------

df_loanData.count()

# COMMAND ----------

len(df_loanData.rdd.glom().collect())

# COMMAND ----------

for partitionNUm, partition in enumerate(df_loanData.rdd.glom().collect()):
    print(f'Length of partition {partitionNUm}: {len(partition)}')

# COMMAND ----------

# MAGIC %md 
# MAGIC #### Adaptive query execution
# MAGIC - Disable adaptive query execution
# MAGIC - Repartition based on a specific column
# MAGIC - Explore each partition size using the len(df.rdd.glom().collect())

# COMMAND ----------

spark.conf.set("spark.sql.adaptive.enabled", False)

# COMMAND ----------

display(
    df_loanData
    .select(F.col("Degree"))
    .distinct()
)

# COMMAND ----------

df_loanData = df_loanData.repartition("Degree")

# COMMAND ----------

print(df_loanData.rdd.getNumPartitions())

# COMMAND ----------

for partitionNum, partition in enumerate(df_loanData.rdd.glom().collect()):
    print(f'Length of partition {partitionNum}: {len(partition)}')

# COMMAND ----------

spark.conf.get("spark.sql.shuffle.partitions")

# COMMAND ----------

# MAGIC %md
# MAGIC #### The above result is due to the fact that the default number of partitions in Spark is 200. 
# MAGIC - Use the spark.conf.set("spark.sql.shuffle.partitions", 3) command to set the number of partitions to 3, and then repeat the whole process
# MAGIC - Since the number of records for each unique value in degree column is not equal, repartitioning based on this column would lead to a data skew. However, this is still good practice to understand how partitioning works in Spark. 

# COMMAND ----------

spark.conf.set("spark.sql.shuffle.partitions", 3)

# COMMAND ----------

df_loanData = df_loanData.repartition("Degree")

# COMMAND ----------

print(df_loanData.rdd.getNumPartitions())

# COMMAND ----------

for partitionNum, partition in enumerate(df_loanData.rdd.glom().collect()):
    print(f'Length of partition {partitionNum}: {len(partition)}')

# COMMAND ----------

display(
    df_loanData
    .groupBy(F.col("Degree"))
    .count()
)
