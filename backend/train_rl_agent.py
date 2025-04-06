import pandas as pd
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from stock_trading_env import StockTradingEnv
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import joblib

# Load your data
raw_data = pd.read_csv("data/AAPL_data.csv")

# Load model and scaler
lstm_model = load_model("models/lstm_model_fixed.h5")
scaler = joblib.load("models/scaler.pkl")

# Preprocess for LSTM (same time_steps used in training)
def create_lstm_features(df, time_steps=60):
    features = df.drop(columns=['Date'])  # Drop non-numeric
    features_scaled = scaler.transform(features)

    sequences = []
    for i in range(len(features_scaled) - time_steps):
        seq = features_scaled[i:i + time_steps]
        sequences.append(seq)

    return np.array(sequences)

# Add LSTM predictions to DataFrame
def add_lstm_signals(df):
    df = df.copy()
    time_steps = 60
    X_seq = create_lstm_features(df, time_steps)
    predictions = lstm_model.predict(X_seq)
    predictions = np.squeeze(predictions)

    # Pad with zeros to align
    lstm_signals = np.concatenate([np.zeros(len(df) - len(predictions)), predictions])
    df['lstm_signal'] = lstm_signals
    return df

# Enhance the data
enhanced_df = add_lstm_signals(raw_data)

# Create the environment
env = DummyVecEnv([lambda: StockTradingEnv(enhanced_df)])

# Train the RL agent
model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

# Save the trained model
model.save("models/lstm_model.keras", save_format="keras")
print("✅ RL model trained and saved successfully.")
