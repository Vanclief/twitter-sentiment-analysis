import sys
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pymongo import MongoClient
from poloniex import Poloniex

polo = Poloniex()

# Mongo DB
client = MongoClient()
db = client["cryto_trading_bot"]

def date_to_timestamp(date):
    return int(time.mktime(date.timetuple())) - 18000

def get_twitter_dataset(start, end):

    tweets = db.bitcoin_sentiment.find(
            {'created': {'$gte': start, '$lt': end}}
            )

    df = pd.DataFrame(
            list(tweets)
            )

    df = df.set_index('created')

    compound = df['s_compound']
    compound = compound.resample("5T").mean().fillna(0)

    return compound

def get_poloniex_dataset(start, end):
    start_timestamp = date_to_timestamp(start)
    end_timestamp = date_to_timestamp(end)

    chart_data = (polo.returnChartData (
        'USDT_BTC', 300, start_timestamp, end_timestamp
        ))

    pol_data = pd.DataFrame(chart_data)

    pol_data['date'] = map (
            lambda x: datetime.fromtimestamp(int(x)) + timedelta(hours=5),
            pol_data['date'])

    pol_data = pol_data.set_index('date')
    average = pol_data['weightedAverage'].astype(float)

    return average

def main(start_time, end_time):

    start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    twitter_ds = get_twitter_dataset(start, end)
    poloniex_ds = get_poloniex_dataset(start, end)


    if (not twitter_ds.empty):
       ax1 = twitter_ds.plot(
                kind='line',
                color='blue')
       ax1.set_ylabel('Twitter Sentiment', color='b')
       ax2 = ax1.twinx()
       ax2.set_ylabel('Bitcoin Price', color='r')
       poloniex_ds.plot(
               kind = 'line',
               color ='red',
               ax=ax2
               )
       plt.show()
    else:
        print('Not enough data for that timeline')

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print ("ERROR: Usage tweet_sentient.py <start date> <end date>")
    else:
        main(sys.argv[1], sys.argv[2])
