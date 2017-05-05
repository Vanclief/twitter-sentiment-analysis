import json
import re
import sys
import os
import Levenshtein as lv
import calendar, time
import pandas as pd
from datetime import datetime
from nltk.stem.snowball import SnowballStemmer
from pymongo import MongoClient

# MongoDB
client = MongoClient()
db = client["cryto_trading_bot"]
db.bitcoin_processed_tweets.ensure_index("id", unique=True, dropDups=True)

class TweetProcessor:
    """
    Input:
        Array of lines made from tweets in json format

    Attributes:
        data: Dataframe of tweets

    Proccedures:
        1. Removing all extra whitespaces
        2. Change the text to lowercase
        3. Remove non-alphabetical characters
        4. Remove tweet duplicates

    Output: Cleaned Dataframe of tweets
    """

    levenshtein_distance = 20
    stemmer = SnowballStemmer("english")

    def __init__(self, data):
        self.data = data

    def __remove_whitespaces(self):
        """ Removes all the tralling whitespaces """
        self.data['text'] = map (lambda tweet: re.sub( '\s+', ' ', tweet).strip(), self.data['text'])
        print ("Removed whitespaces")

    def __lowercase(self):
        """ Changes to lowercase the data """
        self.data['text'] = map (lambda tweet: tweet.lower(), self.data['text'])
        print ("Lowercased")

    def __filter_alphabetic(self):
        """ Remove all non alphabetical characters """
        self.data['text'] = map (lambda tweet: tweet.encode('ascii', 'ignore'), self.data['text'])
        print ("Filtered alphabetic")

    def __filter_duplicates(self):
        """ Remove all duplicates from the file by applying Leveshtien Distance to the string"""
        duplicates = set()
        for i, a in enumerate(self.data['text']):
            os.system('clear')
            print ("Filtered: " + str(100 * i / len(self.data['text'])) + " %")
            for j, b in enumerate(self.data['text']):
                if (i != j and lv.distance(a, b) < self.levenshtein_distance):
                    duplicates.add(j + 1)
        self.data = self.data.drop(duplicates, errors='ignore')
        self.data = self.data.reset_index(drop=True)
        print ("Filtered duplicates")

    def __stem_data(self):
        """ Apply steeming to data """
        self.data['stemmed'] = self.data["text"].apply(lambda tweet: " ".join([self.stemmer.stem(word) for word in tweet.split(" ")]))
        print ("Stemmed")

    def process_data(self):
        self.__remove_whitespaces()
        self.__lowercase()
        self.__filter_alphabetic()
        self.__filter_duplicates()
        self.__stem_data()

        return self.data

def main(start_time, end_time):

    start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    tweets = db.bitcoin_tweets.find({'created': {'$gte': start, '$lt': end}})

    data = pd.DataFrame(list(tweets))

    if (not data.empty):

        tp = TweetProcessor(data)
        print ('Processing Data...')
        data = tp.process_data()
        os.system('clear')
        print ('Done')
        new_data = data.to_dict('records')

        for col in new_data:

            if (not db.bitcoin_processed_tweets.find_one({'id': { "$eq": col['id']}})):
                del col['_id']
                db.bitcoin_processed_tweets.save(col)

        print ('Saved')

    else:
        print('Not enough data for that timeline')

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print ("ERROR: Usage tweet_processor.py <start date> <end date>")
    else:
        main(sys.argv[1], sys.argv[2])
