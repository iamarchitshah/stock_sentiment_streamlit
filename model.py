import numpy as np
import pandas as pd
import joblib
from tensorflow.keras.models import load_model

model = load_model("lstm_stock_model.h5")
scaler = joblib.load("scaler.save")

def predict_lstm(df, time_steps=60, days=7):
    df = df[['Open', 'High', 'Low', 'Close']]
    scaled_data = scaler.transform(df)
    last_seq = scaled_data[-time_steps:]
    pred_scaled = model.predict(np.expand_dims(last_seq, axis=0))[0].reshape(days, 4)
    combined = np.vstack([scaled_data[-days:], pred_scaled])
    unscaled = scaler.inverse_transform(combined)[-days:]
    return pd.DataFrame(unscaled, columns=['Open', 'High', 'Low', 'Close'])