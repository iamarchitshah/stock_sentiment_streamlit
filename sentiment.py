import json, tweepy
from textblob import TextBlob

def fetch_tweets(ticker, count=50):
    with open("twitter_api_keys.json") as f:
        keys = json.load(f)
    auth = tweepy.OAuth1UserHandler(keys['consumer_key'], keys['consumer_secret'],
                                    keys['access_token'], keys['access_token_secret'])
    api = tweepy.API(auth)
    return [t.text for t in api.search_tweets(q=f"{ticker} stock", count=count, lang="en")]

def analyze_sentiment(tweets):
    scores = [TextBlob(t).sentiment.polarity for t in tweets]
    avg = sum(scores) / len(scores)
    if avg > 0.1: return "Positive"
    elif avg < -0.1: return "Negative"
    else: return "Neutral"

def sentiment_breakdown(tweets):
    score = {"positive": 0, "neutral": 0, "negative": 0}
    for t in tweets:
        p = TextBlob(t).sentiment.polarity
        if p > 0.1: score["positive"] += 1
        elif p < -0.1: score["negative"] += 1
        else: score["neutral"] += 1
    return score