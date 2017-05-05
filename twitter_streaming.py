import os
import sys
import time
import json
import datetime
from pymongo import MongoClient
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# MongoDB
client = MongoClient()
db = client["cryto_trading_bot"]
db.bitcoin_tweets.ensure_index("id", unique=True, dropDups=True)
collection = db.bitcoin_tweets

# Keywords
keywords = ['$btc', '#btc', 'btc', '$bitcoin', '#bitcoin', 'bitcoin']

# Only grab tweets in english
language = ['en']

# Twitter API stuff
consumer_key = "e6nP2qftfJlcbvbrrL0JlWPHn"
consumer_secret = "SXVyBdbNyhohxO1EQGBKq8QlY83e17FUWvaeQJtWhvCzcDnpu3"
access_token = "2397402739-vu0AUKOY49clNceFSbrGk4Onn7peL0XzCQvLAgP"
access_token_secret = "esHGDDtvAm2jLSoyemApDGmI29ZLODfSLienoLgl1a4rJ"

class StdOutListener(StreamListener):

    def on_data(self, data):

        t = json.loads(data)

        tweet_id = t['id_str']
        username = t['user']['screen_name']
        followers = t['user']['followers_count']
        text = t['text']
        hashtags = t['entities']['hashtags']
        timestamp = t['created_at']
        language = t['lang']

        created = datetime.datetime.strptime(timestamp, '%a %b %d %H:%M:%S +0000 %Y')

        tweet = {'id':tweet_id,
                'username':username,
                'followers':followers,
                'text':text,
                'hashtags':hashtags,
                'language':language,
                'created':created
                }

        os.system('clear')

        if collection.find_one({'id': { "$eq": tweet_id}}):
            print ('Tweet already exists!')
        else:
            print("New tweet! " + tweet_id)
            collection.save(tweet)

        return True

    def on_error(self, status):
        print status
        return True

if __name__ == '__main__':
    while True:
        l = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        stream = Stream(auth, l)
        stream.filter(track=keywords, languages=language)

