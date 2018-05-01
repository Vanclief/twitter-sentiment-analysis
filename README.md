# CryptoTweetSentiment

This was my first attempt at applying sentiment analysis for crypto-trading. If you are interested in this, I recommend you check out [this](https://github.com/Vanclief/algo-trading-crypto) instead.

Code is hardcoded to gather twitter data for bitcoin, but that can be easily modified to support other coins. I have abandoned this project, but feel free to toy with this.

## Dependencies:

* [MongoDB](https://docs.mongodb.com/manual/installation/)

* [Python2.7](https://www.python.org/downloads/)


## Install requirements
`pip install -r requirements.txt`

## Collecting tweets

You will need to collect a sample of tweets before you can apply sentiment analysis. In order to start collecting Tweets run:

`python twitter_streaming.py`

## Analysing tweets

Once you have collected enough information for the desired dateframe, you can run the main file. Main will call the necessary scripts in order to clean, analyze and graph the data.

`python __main__.py <start-date> <end-date>`

Example:

`python __main__.py "2017-05-02 00:00:00" "2017-12-21 00:00:00`

This will:

1. run `tweet_processor.py` which will:

* Clean the data

* Filter duplicates and retweets using Levenshtein distance (This step takes the longest)

2. run `tweet_sentiment.py` which will:

* Apply Valence Aware Dictionary and Sentient Reasoner analysis to the text of the tweets. This will return a vector that contains the normalized values for the amount of positivity, negativity and neutrality of the tweet, which will be compounded to get a score from -1 to 1 on the sentiment of the tweet. Scores over 0.5 are considered positive, while scores under -0.5 are considered negative.

* Create two new collections on the MongoDB. One with the tweets with raw text, one with a stemmed version.

3. run `grapher.py` which will:

* Graph the price of bitcoin between the timespan of the collected tweets against the mean of the sentiment of the tweets

You can run any of the scripts by itself as long as you give the desired timespan.
