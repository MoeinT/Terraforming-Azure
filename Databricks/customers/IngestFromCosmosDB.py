# Databricks notebook source
import pyspark.sql.types as T
import pyspark.sql.functions as F

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
    
    @staticmethod
    def WriteToDeltaTable(df, mode, targetLoc):
        return (
            df
            .write
            .mode(mode)
            .format("delta")
            .saveAsTable(targetLoc)
        )

# COMMAND ----------

cosmosEndpoint = dbutils.secrets.get(scope = "kv-scope", key = "cosmosdb-endpoint")
cosmosMasterKey = dbutils.secrets.get(scope = "kv-scope", key = "cosmosdb-primaryKey")
database = "Families-dev"
container = "superstore-container-dev"

# Configure Catalog Api to be used
spark.conf.set("spark.sql.catalog.cosmosCatalog", "com.azure.cosmos.spark.CosmosCatalog")
spark.conf.set("spark.sql.catalog.cosmosCatalog.spark.cosmos.accountEndpoint", cosmosEndpoint)
spark.conf.set("spark.sql.catalog.cosmosCatalog.spark.cosmos.accountKey", cosmosMasterKey)

cosmosobj = ConnToCosmosDB(
    cosmosEndpoint = cosmosEndpoint,
    cosmosMasterKey = cosmosMasterKey,
    database = database,
    container = container
)

df_superstore = cosmosobj.getData
cosmosobj.WriteToDeltaTable(df_superstore, mode = "overwrite", targetLoc = "CustomerData.superstore")
