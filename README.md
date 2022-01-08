# Twitterstream Sentiment-Analysis with Kafka, Spark , Elasticsearch & kibanna
Reading the Twitterstream from the Twitter-API with Kafka and stream them into a Spark-Cluster to process it by doing SENTIMENT analysis of hash tags in twitter data in real-time. For example, we want to do the sentiment analysis for all the tweets  #coronavirus

![github-logo](https://github.com/alandtsang/README/blob/master/images/github-logo.png "Optional title")
## Things you need
- Installed  Kafka
- Installed Apache Spark
- Installed Elasticsearch & Kibana (If you want to visualize results)

## Twitter Modules

- Tweepy (And your own pair of API Keys from Twitter)
- Kafka-Python
- Pyspark
- Elasticsearch
- NLTK
- textblob
## Steps

1. Twitter Api
 collecting tweets and sends them to Kafka for analytics. The scraper is a standalone program written in PYTHON and performs the followings:

a. Collects tweets in real-time with particular hash tags. For example, we

will collect all tweets with #coronavirus.

b. After filtering, it send them to Kafka 


2. Kafka
You need to install Kafka and run Kafka Server with Zookeeper. You should create a dedicated channel/topic for data transport

3. Spark Streaming
In Spark Streaming, Kafka consumer is created that periodically collect filtered tweets from scrapper. For each hash tag, perform sentiment analysis using Sentiment Analyzing tool.

4. Sentiment Analyzer
Sentiment Analysis is the process of determining whether a piece of writing is positive, negative, or neutral. 



4. Elasticsearch
You need to install the Elasticsearch and run it to store the tweets and their sentiment information for further visualization purpose.

You can point http://localhost:9200 to check if it's running.



5. Kibana
Kibana is a visualization tool that can explore the data stored in elasticsearch. In the project, instead of directly output the result, visualization tool is used to show the tweets sentiment classification result in a real-time manner. 
![github-logo](https://github.com/nesrine378/sentiment-analysis-twitter/blob/main/dashboard.png )



