import json
import datetime
from pymongo import MongoClient

# MongoDB
client = MongoClient()
db = client["cryto_trading_bot"]
# collection = db.bitcoin_tweets
collection = db.bitcoin_processed_tweets

try:
    start = datetime.datetime(2017, 5, 2, 1, 35, 6, 764)
    end = datetime.datetime(2017, 5, 2, 6, 55, 3, 381)
    tweets = collection.find({'created': {'$gte': start, '$lt': end}})
    for tweet in tweets:
	# print (tweet['text'])
	print (tweet)

except Exception, e:
    print str(e)
