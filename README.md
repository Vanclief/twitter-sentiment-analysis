# CrytoTweetSentiment

This project is focused on performing sentiment analysis for the cryptocurrency bitcoin, but can easily be expanded to other coins. Currently it only gathers data from Twitter.

## Justification:

Cryptocurrencies have been on the rise for the past years. Its value is completely defined by speculation of how much they can be worth. As such their exchange rates are very volatile, and very unpredictable.

Twitter is one of the most popular social media networks there is, and its an outlet though which millions of people broadcast their thoughts, fears and opinions on any topic of their interest.

The goal of this project is to determine if we analyze this publicly available data to develop cryto trading strategies or algorithms that are profitable.

## Documentation:

### Dependencies:

* [MongoDB](https://docs.mongodb.com/manual/installation/)

* [Python2.7](https://www.python.org/downloads/)


### Install requirements
`pip install -r requirements.txt`

### Collecting tweets

CrytoTweetSentiment TM requires to collect a sample of tweets so it can apply sentiment analysis to it. In order to start collecting Tweets run:

`python twitter_streaming.py`

### Analysing tweets

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

## Analysis:

The hypothesis seemed to fail as there is no correlation found yet. However, more analysis has to be made in order to obtain the right configuration parameters and more sampling has to be done.

## Variables to consider:

* Try another analysis without lowercasing tweets, and allowing ASCII. VADER supports the analysis of words in uppercase and emoticons.

* The current implementation uses the non-stemmed data, there seemed to be quite a difference between the two.

# Biography

* http://www.cs.cmu.edu/~nasmith/papers/oconnor+balasubramanyan+routledge+smith.icwsm10.pdf

* http://cs229.stanford.edu/proj2015/029_report.pdf
