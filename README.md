# CryptoTweetSentiment

**Note:** Project is no longer maintained, will probably fail to run because dependencies have been updated and most likely contain breaking changes.

This was my first attempt at applying sentiment analysis for crypto-trading. If you are interested in this, I recommend you check out [this](https://github.com/Vanclief/algo-trading-crypto) instead.

Code is hardcoded to gather twitter data for bitcoin, but that can be easily modified to support other coins. I have abandoned this project, but feel free to toy with this.

## Dependencies:

- [MongoDB](https://docs.mongodb.com/manual/installation/)

- [Python2.7](https://www.python.org/downloads/)

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

- Clean the data

- Filter duplicates and retweets using Levenshtein distance (This step takes the longest)

2. run `tweet_sentiment.py` which will:

- Apply Valence Aware Dictionary and Sentient Reasoner analysis to the text of the tweets. This will return a vector that contains the normalized values for the amount of positivity, negativity and neutrality of the tweet, which will be compounded to get a score from -1 to 1 on the sentiment of the tweet. Scores over 0.5 are considered positive, while scores under -0.5 are considered negative.

- Create two new collections on the MongoDB. One with the tweets with raw text, one with a stemmed version.

3. run `grapher.py` which will:

- Graph the price of bitcoin between the timespan of the collected tweets against the mean of the sentiment of the tweets

You can run any of the scripts by itself as long as you give the desired timespan.

## Pairing with GetXAPI for Cheaper Read Operations (Optional)

For users who need a cheaper or higher-rate-limit option for read-only Twitter (X) operations such as tweet search, profile lookup, and follower lists, this project can be paired with [GetXAPI](https://getxapi.com), a budget Twitter / X data API priced at $0.05 per 1K tweets versus the official X API basic tier at $200 / month.

Two integration patterns:

1. **Run side-by-side in your AI client.** Keep this project for its primary workflow and add the [official GetXAPI MCP server](https://github.com/getxapi/getxapi-mcp) for read-heavy tasks. Each tool name routes to the backend best suited for that operation.

2. **Add a backend toggle.** For a code-level reference of an optional alternative backend behind a single env variable, see the [PR pattern merged into a sibling project](https://github.com/GenAIwithMS/twitter-mcp/pull/3).

GetXAPI quick start:

- Signup with $0.50 free credit (no card required): https://getxapi.com/signup
- Official GetXAPI MCP server: https://github.com/getxapi/getxapi-mcp
- npm: `@getxapi/mcp`
- Pay-per-call pricing: $0.001 / call, $0.05 / 1K tweets

This pairing is fully optional. No behavior change for existing users.

