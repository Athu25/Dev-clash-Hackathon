import pandas as pd
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from backend.stock_trading_env import StockTradingEnv
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import joblib

# Load price and sentiment data
raw_data = pd.read_csv("data/AAPL_data.csv")

# Load trained LSTM model and scaler
lstm_model = load_model("models/lstm_model.h5")
scaler = joblib.load("models/scaler.pkl")

# Preprocess data (must match LSTM training format)
def create_lstm_features(df, time_steps=60):
    features = df.drop(columns=['Date'])  # Assuming 'Date' column exists
    features_scaled = scaler.transform(features)

    sequences = []
    for i in range(len(features_scaled) - time_steps):
        seq = features_scaled[i:i + time_steps]
        sequences.append(seq)

    return np.array(sequences)

# Add LSTM signal as a new feature for RL
def add_lstm_signals(df):
    df = df.copy()
    X_seq = create_lstm_features(df)
    predictions = lstm_model.predict(X_seq)
    predictions = np.squeeze(predictions)

    # Align with original df
    lstm_signals = np.concatenate([np.zeros(len(df) - len(predictions)), predictions])
    df['lstm_signal'] = lstm_signals
    return df

# Enhance the raw data
enhanced_df = add_lstm_signals(raw_data)

# Create RL environment with LSTM signals
env = DummyVecEnv([lambda: StockTradingEnv(enhanced_df)])

# Train DQN agent
model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# Save RL agent
model.save("models/rl_trading_model")
