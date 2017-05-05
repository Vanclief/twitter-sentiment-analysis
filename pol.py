import sys
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pymongo import MongoClient
from poloniex import Poloniex

polo = Poloniex()

def main(start_time, end_time):

    start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    start_timestamp = int(time.mktime(start.timetuple())) - 18000
    end_timestamp = int(time.mktime(end.timetuple())) - 18000

    print start_timestamp
    print end_timestamp

    print (polo.returnChartData ('USDT_BTC', 300, start_timestamp, end_timestamp))


if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print ("ERROR: Usage tweet_sentient.py <start date> <end date>")
    else:
        main(sys.argv[1], sys.argv[2])
