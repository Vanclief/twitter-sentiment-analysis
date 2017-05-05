import sys
import os
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

client = MongoClient()
db = client["cryto_trading_bot"]

class TweetSentiment:
    """
    Input:
        Dataframe of tweets, one normal and one stemmed
    """

    analyzer = SentimentIntensityAnalyzer()

    def __init__(self, data):
        self.data = data

    def analyze(self):
        labels = ['neg', 'neu', 'pos', 'compound']

        for label in labels:
            self.data['s_' + label] = self.data['text'].map(
                   lambda tweet: self.analyzer.polarity_scores(tweet)[label])
            self.data['steam_' + label] = self.data['stemmed'].map(
                    lambda tweet: self.analyzer.polarity_scores(tweet)[label])
        return self.data


def main(start_time, end_time):

    start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    tweets = db.bitcoin_processed_tweets.find({'created': {'$gte': start, '$lt': end}})

    data = pd.DataFrame(list(tweets))

    if (not data.empty):
        ts = TweetSentiment(data)
        print ('Processing Data...')
        data = ts.analyze()
        print ('Done')
        new_data = data.to_dict('records')

        for col in new_data:
            if (not db.bitcoin_sentiment.find_one({'id': { "$eq": col['id']}})):
                del col['_id']
                db.bitcoin_sentiment.save(col)

        print ('Saved')
    else:
        print('Not enough data for that timeline')

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print ("ERROR: Usage tweet_sentiment.py <start date> <end date>")
    else:
        main(sys.argv[1], sys.argv[2])
