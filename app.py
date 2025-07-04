import streamlit as st
import yfinance as yf
from utils.model import predict_lstm
from utils.sentiment import fetch_tweets, analyze_sentiment, sentiment_breakdown
from utils.chart import plot_predictions, plot_sentiment_pie

st.set_page_config(page_title="Stock Forecast + Sentiment", layout="centered")
st.title("📈 Stock Price Forecast & 🗣️ Sentiment Analysis")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, INFY.NS)")

if ticker:
    df = yf.download(ticker, period="1y")[['Open', 'High', 'Low', 'Close']]
    lstm_pred = predict_lstm(df)
    tweets = fetch_tweets(ticker)
    sentiment = analyze_sentiment(tweets)
    pie_data = sentiment_breakdown(tweets)

    st.subheader("💹 7-Day Forecast (Close Price)")
    st.plotly_chart(plot_predictions(df, lstm_pred), use_container_width=True)

    st.subheader(f"🧠 Sentiment: {sentiment}")
    st.plotly_chart(plot_sentiment_pie(pie_data), use_container_width=True)

    st.download_button("📥 Download Predictions as CSV", data=lstm_pred.to_csv().encode('utf-8'),
                       file_name="lstm_predictions.csv", mime="text/csv")