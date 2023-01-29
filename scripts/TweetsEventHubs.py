import asyncio
import configparser
import json

import pytz
import tweepy
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient


class MyStream(tweepy.StreamingClient):
    def __init__(self, bearer_token, **kwargs):
        self.eventhub_name = kwargs.pop("eventhub_name")
        self.eventhubs_ns_connstr = kwargs.pop("eventhubs_ns_connstr")
        super(MyStream, self).__init__(bearer_token, **kwargs)

    def on_connect(self):
        print("Connected")

    # Retrieve the tweets
    def on_tweet(self, tweet):

        my_tweet = json.dumps(
            {
                "user_id": tweet.author_id,
                "created_at": tweet.created_at.astimezone(pytz.timezone("Europe/Paris")).strftime("%Y-%m-%d %H:%M:%S"),
                "tweet_type": MyStream.get_tweet_type(tweet.referenced_tweets),
                "lang": tweet.lang,
                "tweet": tweet.text,
                "hashtags": MyStream.get_hashtags(tweet.entities),
            },
            default=str,
        )

        # Call the Eventhub function
        self.send_eventhub(my_tweet)

    # Send streams to Azure Eventhub
    def send_eventhub(self, tweet):
        async def run():
            producer = EventHubProducerClient.from_connection_string(
                conn_str=self.eventhubs_ns_connstr, eventhub_name=self.eventhub_name
            )
            async with producer:
                event_data_batch = await producer.create_batch()
                event_data_batch.add(EventData(tweet))
                await producer.send_batch(event_data_batch)
                print(f"Event successfully sent to Azure EventHubs!")

        asyncio.run(run())

    @staticmethod
    def get_hashtags(entities: dict) -> str:

        if "hashtags" in entities.keys():
            l_tags = []
            for hashtag in entities["hashtags"]:
                if "tag" in hashtag.keys():
                    l_tags.append(hashtag["tag"])
            return ", ".join(l_tags)
        else:
            return ""

    @staticmethod
    def get_tweet_type(referenced_tweets: list[dict]) -> str:
        l_types = []
        if referenced_tweets != None:
            for item in referenced_tweets:
                if "type" in item.keys():
                    l_types.append(item["type"])
                else:
                    return ""
            return ", ".join(l_types)
        else:
            return "tweeted"


if __name__ == "__main__":

    # Initial config
    config = configparser.ConfigParser(interpolation=None)
    config.read("config.ini")
    eventhubs_ns_connstr = config["Azure"]["eventhubs_ns_connstr"]
    bearer_token = config["Azure"]["bearer_token"]
    eventhub_name = config["Azure"]["eventhub_name"]

    # Search terms
    search_terms = [
        "(python OR #python OR dataengineering OR #dataengineering)"
    ]

    # Define a stream object
    stream = MyStream(
        bearer_token=bearer_token,
        eventhub_name=eventhub_name,
        eventhubs_ns_connstr=eventhubs_ns_connstr,
    )

    # Add rules to the stream
    for term in search_terms:
        stream.add_rules(tweepy.StreamRule(term))

    # Define the filters
    stream.filter(
        tweet_fields=[
            "lang",
            "entities",
            "author_id",
            "created_at",
            "referenced_tweets",
        ]
    )