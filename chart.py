import plotly.graph_objs as go
import pandas as pd

def plot_predictions(actual_df, pred_df):
    future_dates = pd.date_range(start=actual_df.index[-1], periods=len(pred_df)+1, freq='B')[1:]
    trace1 = go.Scatter(x=actual_df.index, y=actual_df['Close'], name="Historical Close")
    trace2 = go.Scatter(x=future_dates, y=pred_df['Close'], name="Predicted Close")
    return go.Figure(data=[trace1, trace2])

def plot_sentiment_pie(scores):
    return go.Figure(data=[go.Pie(labels=list(scores.keys()), values=list(scores.values()))])