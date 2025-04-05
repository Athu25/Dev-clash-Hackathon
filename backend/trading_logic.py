import pandas as pd
import numpy as np
import os
from tensorflow.keras.models import load_model
from utils import preprocess_data  # assume this handles scaling and shaping

# Load LSTM model
model_path = os.path.join('models', 'lstm_model.h5')
model = load_model(model_path)

# Load and preprocess data
def generate_trade_signal():
    data_path = os.path.join('data', 'AAPL_data.csv')
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()

    # Preprocess the data (scaling, creating sequences, etc.)
    X, latest_features = preprocess_data(df)

    # Make prediction on latest feature sequence
    prediction = model.predict(latest_features)
    predicted_class = int(prediction[0][0] > 0.5)
    confidence = float(prediction[0][0]) if predicted_class == 1 else 1 - float(prediction[0][0])
    
    action = "BUY" if predicted_class == 1 else "SELL"

    return {
        "symbol": "AAPL",
        "action": action,
        "confidence": round(confidence, 2)
    }
