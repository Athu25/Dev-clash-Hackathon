import pandas as pd
import numpy as np
import os
from tensorflow.keras.models import load_model
from utils import preprocess_data
from sentiment_analysis import get_sentiment_score
from rl_predictor import rl_predict_action  # Assume this returns "BUY" or "SELL"

# Load LSTM model
model_path = os.path.join('models', 'lstm_model.h5')
model = load_model(model_path)

def generate_trade_signal(symbol="AAPL"):
    # Load historical stock data
    data_path = os.path.join('data', f'{symbol}_data.csv')
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()

    # Preprocess data for LSTM
    X, latest_features = preprocess_data(df)

    # Make prediction using LSTM model
    prediction = model.predict(latest_features)
    predicted_class = int(prediction[0][0] > 0.5)
    confidence = float(prediction[0][0]) if predicted_class == 1 else 1 - float(prediction[0][0])

    # Sentiment analysis for the stock
    sentiment_score = get_sentiment_score(symbol)  # e.g., returns float between -1 and 1

    # Reinforcement learning agent's action
    rl_action = rl_predict_action(df)  # e.g., returns "BUY" or "SELL"

    # Combine signals (simple rule: agree or majority wins)
    lstm_action = "BUY" if predicted_class == 1 else "SELL"
    combined_action = "BUY" if [lstm_action, rl_action, "BUY" if sentiment_score > 0 else "SELL"].count("BUY") > 1 else "SELL"

    return {
        "symbol": symbol,
        "action": combined_action,
        "confidence": round(confidence, 2),
        "lstm_action": lstm_action,
        "rl_action": rl_action,
        "sentiment": sentiment_score
    }
