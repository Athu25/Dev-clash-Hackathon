import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sentiment_analysis import get_sentiment_score
from rl_predictor import get_rl_action
from utils import preprocess_data

# Load LSTM model once
lstm_model = load_model("models/lstm_model.h5")

def generate_trade_signal(symbol):
    # Load and preprocess stock data
    df = pd.read_csv(f"data/{symbol}_data.csv")
    X_input = preprocess_data(df)

    # Get LSTM prediction
    lstm_pred = lstm_model.predict(X_input)
    predicted_move = np.argmax(lstm_pred)  # or use threshold if binary

    # Get sentiment score (e.g., -1 to 1)
    sentiment = get_sentiment_score(symbol)

    # Combine into state vector for RL
    state = np.array([predicted_move, sentiment])

    # Get action from RL agent: 0 = Hold, 1 = Buy, 2 = Sell
    action = get_rl_action()

    # Return action as a trade signal
    if action == 1:
        return "buy"
    elif action == 2:
        return "sell"
    else:
        return "hold"
