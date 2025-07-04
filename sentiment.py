import tweepy
from textblob import TextBlob
import streamlit as st

# Load Twitter API credentials from Streamlit Secrets
keys = {
    "consumer_key": st.secrets["consumer_key"],
    "consumer_secret": st.secrets["consumer_secret"],
    "access_token": st.secrets["access_token"],
    "access_token_secret": st.secrets["access_token_secret"]
}

# Authenticate with Twitter
auth = tweepy.OAuth1UserHandler(
    keys["consumer_key"],
    keys["consumer_secret"],
    keys["access_token"],
    keys["access_token_secret"]
)
api = tweepy.API(auth)

# Fetch tweets related to the given stock ticker
def fetch_tweets(ticker, count=50):
    query = f"{ticker} stock"
    tweets = api.search_tweets(q=query, lang="en", count=count, tweet_mode='extended')
    return [tweet.full_text for tweet in tweets]

# Analyze average sentiment polarity
def analyze_sentiment(tweets):
    scores = [TextBlob(t).sentiment.polarity for t in tweets]
    if not scores:
        return "Neutral"
    avg = sum(scores) / len(scores)
    if avg > 0.1:
        return "Positive"
    elif avg < -0.1:
        return "Negative"
    else:
        return "Neutral"

# Breakdown of sentiment counts for pie chart
def sentiment_breakdown(tweets):
    breakdown = {"positive": 0, "neutral": 0, "negative": 0}
    for t in tweets:
        polarity = TextBlob(t).sentiment.polarity
        if polarity > 0.1:
            breakdown["positive"] += 1
        elif polarity < -0.1:
            breakdown["negative"] += 1
        else:
            breakdown["neutral"] += 1
    return breakdown
