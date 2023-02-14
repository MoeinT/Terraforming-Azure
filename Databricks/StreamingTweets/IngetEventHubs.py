# Databricks notebook source
dbutils.widgets.dropdown("env", "dev", ["dev", "test", "qa", "prod"])

# COMMAND ----------

import pyspark.sql.types as T
import pyspark.sql.functions as F
from delta.tables import DeltaTable

# COMMAND ----------

class StreamTweets:
    def __init__(self, namespaceConnStr: str, eventhubName: str, schema: str, targetDatabase = "Tweets") -> None:
        self.namespaceConnStr = namespaceConnStr
        self.eventhubName = eventhubName
        self.schema = schema
        self.database = targetDatabase
    
    @property
    def EventHubsConfigs(self) -> dict:
        return (
            {
                'eventhubs.connectionString' : sc._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(self.namespaceConnStr + ";EntityPath=" + self.eventhubName)
            }
        ) 
    
    @property
    def InputDF(self):
        return (
            (
                spark
                .readStream
                .format("eventhubs")
                .options(**self.EventHubsConfigs)
                .load()

                .select(F.col("body").cast(T.StringType()))
                .select(F.from_json(F.col("body"), self.schema).alias("events"))
                .select("events.*")
            )
        )
    
    def WriteToDeltaTable(self): 
        (
            self.InputDF
            .writeStream
            .format("delta")
            .outputMode("append")
            .option("checkpointLocation", f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/TweetsStream.checkpoint')
            .option("path", f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/TweetsStream.delta')
            .trigger(processingTime = "5 seconds")
            .table(f'{self.database}.Covid19')
        )
    
    @staticmethod
    def upsertToDelta(microBatchOutputDF, batchId):
        
        dl_NumberOfTweets = DeltaTable.forName(spark, "Tweets.NumberOfTweets") 
        
        (
            dl_NumberOfTweets.alias('target')
            .merge
            (
                microBatchOutputDF.alias('update'), 
                "target.StartEvent = update.StartEvent and target.EndEvent = update.EndEvent"
            )
            .whenNotMatchedInsertAll()
            .whenMatchedUpdateAll()
            .execute()
        )
        
    
    def UpdateNumberOfTweets(self): 
        (
            self.InputDF
            .groupBy(F.window("created_at", "10 seconds"))
            .count()
            .select(F.col("window.start").alias("StartEvent"), F.col("window.end").alias("EndEvent"), F.col("count").alias("NumberOfTweets"))
            
            .writeStream
            .foreachBatch(StreamTweets.upsertToDelta)
            .outputMode("update")
            .option("checkpointLocation", f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles{dbutils.widgets.get("env")}/NumberOfTweets.checkpoint')
            .option("path", f'/mnt/sadb01{dbutils.widgets.get("env")}/commonfiles-{dbutils.widgets.get("env")}/NumberOfTweets.delta')
            .trigger(processingTime = "15 seconds")
            .start()
        )


# COMMAND ----------

tweetSchema = T.StructType(
    [
        T.StructField("user_id", T.LongType(), True),
        T.StructField("created_at", T.TimestampType(), True),
        T.StructField("tweet_type", T.StringType(), True),
        T.StructField("lang", T.StringType(), True),
        T.StructField("tweet", T.StringType(), True),
        T.StructField("hashtags", T.LongType(), True)
    ]
)

streamobj = StreamTweets(
    namespaceConnStr = dbutils.secrets.get(scope = "kv-scope", key = "eventhubs-ns-connstr"),
    eventhubName = dbutils.secrets.get(scope = "kv-scope", key = "eventhubs-name"),
    schema = tweetSchema
)

df_InputStream = streamobj.InputDF
streamobj.WriteToDeltaTable()
streamobj.UpdateNumberOfTweets()
