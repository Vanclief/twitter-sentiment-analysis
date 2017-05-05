import sys
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pymongo import MongoClient
from poloniex import Poloniex

polo = Poloniex()
client = MongoClient()
db = client["cryto_trading_bot"]

def main(start_time, end_time):

    start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    start_timestamp = int(time.mktime(start.timetuple())) - 18000
    end_timestamp = int(time.mktime(end.timetuple())) - 18000

    tweets = db.bitcoin_sentiment.find({'created': {'$gte': start, '$lt': end}})

    data = pd.DataFrame(list(tweets))
    chart_data = (polo.returnChartData ('USDT_BTC', 300, start_timestamp, end_timestamp))

    pol_data = pd.DataFrame(chart_data)
    pol_data['date'] = map (lambda x: datetime.fromtimestamp(int(x)) + timedelta(hours=5), pol_data['date'])
    pol_data['weightedAverage'] = pol_data['weightedAverage'].astype(float)

    print (pol_data)
    print (data['created'])

    if (not data.empty):
        data.plot(
                x = 'created',
                y = 's_compound',
                kind='bar',
                color='blue')
        pol_data.plot(
                x = 'date',
                y = 'weightedAverage',
                kind = 'line',
                color ='red')
        plt.show()
    else:
        print('Not enough data for that timeline')

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print ("ERROR: Usage tweet_sentient.py <start date> <end date>")
    else:
        main(sys.argv[1], sys.argv[2])
