import pandas as pd
from stable_baselines3 import DQN
from backend.stock_trading_env import StockTradingEnv
from stable_baselines3.common.vec_env import DummyVecEnv

df = pd.read_csv("data/AAPL_data.csv")
env = DummyVecEnv([lambda: StockTradingEnv(df)])

model = DQN.load("models/rl_trading_model")
obs = env.reset()

done = False
while not done:
    action, _ = model.predict(obs)
    obs, reward, done, _ = env.step(action)
    env.envs[0].render()
