import pandas as pd
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from backend.stock_trading_env import StockTradingEnv
from backend.utils import add_sentiment_feature
from datetime import datetime

# Load historical data
df = pd.read_csv("data/AAPL_data.csv")

# Ensure Date is datetime (for sentiment analysis)
df['Date'] = pd.to_datetime(df['Date'])

# Add sentiment scores dynamically
df = add_sentiment_feature(df, stock_symbol='AAPL')

# Drop rows with missing data (just in case)
df.dropna(inplace=True)

# Create environment
env = DummyVecEnv([lambda: StockTradingEnv(df)])

# Define DQN model
model = DQN("MlpPolicy", env, verbose=1)

# Train the agent
print("\n🚀 Training the RL agent...\n")
model.learn(total_timesteps=10000)
print("\n✅ Training completed!\n")

# Save the trained model
model.save("models/rl_trading_model")
print("📦 Model saved at: models/rl_trading_model")
