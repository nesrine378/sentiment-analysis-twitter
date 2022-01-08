from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json
from textblob import TextBlob
from pyspark.sql import *
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
from pyspark.sql.functions import lit
from pyspark.sql.functions import udf
from pyspark.sql.types import *

es = Elasticsearch(hosts=['localhost'], port=9200)

def process(time, rdd):
    print("========= %s =========" % str(time))
    try:
        if rdd.count()==0: raise Exception('Empty')
        sqlContext = getSqlContextInstance(rdd.context)
        df = sqlContext.read.json(rdd)
        df = df.filter("text not like 'RT @%'")
        if df.count() == 0: raise Exception('Empty')
        udf_func = udf(lambda x: dosentiment(x),returnType=StringType())
        df = df.withColumn("sentiment",lit(udf_func(df.text)))
        print(df.take(10))
        results = df.toJSON().map(lambda j: json.loads(j)).collect()
        for result in results:
            result["date"]= datetime.strptime(result["date"],"%Y-%m-%d %H:%M:%S")
            result["sentiment"]=json.loads(result["sentiment"])
        sth2elastic(results,"tweets","doc")
    except Exception as e:
        print(e)
        pass


def main():

    """
    main function initiates a kafka consumer,
    Consumer will consume tweets from producer extracts features, cleanses the tweet text,
    calculates sentiments and loads the data into postgres database
    """

    hashtag = input("Enter the hashtag : ")
    # set-up a Kafka consumer
    consumer = KafkaConsumer("twitter_stream_" + hashtag, auto_offset_reset='earliest')

    for msg in consumer:
        dict_data = json.loads(msg.value)
        tweet = TextBlob(dict_data["text"])
        polarity = tweet.sentiment.polarity
        tweet_sentiment = ""
        if polarity > 0:
            tweet_sentiment = 'positive'
        elif polarity < 0:
            tweet_sentiment = 'negative'
        elif polarity == 0:
            tweet_sentiment = 'neutral'

        # add text & sentiment to es
        es.index(
                    index="tweet_es_" + hashtag + "_index",
                    doc_type="test_doc",
                    body={
                    "author": dict_data["user"]["screen_name"],
                    "date": dict_data["created_at"],
                    "message": dict_data["text"],
                    "sentiment": tweet_sentiment
                    }
                )
        print(str(tweet))
        print('\n')


if __name__ == "__main__":
    main()
