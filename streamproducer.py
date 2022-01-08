from kafka import KafkaProducer
import kafka
import json
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# TWITTER API CONFIGURATIONS


access_token = "1464352002264412161-I28HQtehAqVGFMWy8NyNDm4jy7Yg3q"
access_secret =  "yopiwM0w0jmbDejOB55eCPQbfZlHH8HWRKFm4oesMYuzT"
consumer_key =  "xRvPjnSV3oGSmjL4eHo4ZV3aQ"
consumer_secret =  "4P17sSWoOndGVYqob7Cy4kbBSaYizbVraQ5QsWvZjN5mNOCGWZ"

hashtag = input("Enter the hashtag : ")

# TWITTER API AUTH
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


# Twitter Stream Listener
class KafkaPushListener(StreamListener):
    def __init__(self):
        # localhost:9092 = Default Zookeeper Producer Host and Port Adresses
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    # Get Producer that has topic name is Twitter
    # self.producer = self.client.topics[bytes("twitter")].get_producer()

    def on_data(self, data):
        # Producer produces data for consumer
        # Data comes from Twitter
        self.producer.send("twitter_stream_" + hashtag, data.encode('utf-8'))
        print(data)
        return True

    def on_error(self, status):
        print(status)
        return True


# Twitter Stream Config
twitter_stream = Stream(auth, KafkaPushListener())

hashStr = "#"+ hashtag

# Produce Data that has trump hashtag (Tweets)
twitter_stream.filter(track=[hashStr])
