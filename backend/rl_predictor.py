import pandas as pd
from stable_baselines3 import DQN
from stock_trading_env import StockTradingEnv
from stable_baselines3.common.vec_env import DummyVecEnv

def get_rl_action(df_path="data/AAPL_data.csv", model_path="models/rl_trading_model"):
    # Load data and environment
    df = pd.read_csv(df_path)
    env = DummyVecEnv([lambda: StockTradingEnv(df)])

    # Load trained RL model
    model = DQN.load(model_path)

    # Reset environment and get action
    obs = env.reset()
    action, _ = model.predict(obs, deterministic=True)

    # Optional: You can render once or skip in production
    # env.envs[0].render()

    # Convert numeric action to string
    action_map = {0: "hold", 1: "buy", 2: "sell"}
    return action_map[int(action)]
