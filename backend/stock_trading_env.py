import gym
from gym import spaces
import numpy as np

class StockTradingEnv(gym.Env):
    def __init__(self, df):
        super(StockTradingEnv, self).__init__()
        self.df = df.reset_index(drop=True)
        self.current_step = 0
        self.balance = 10000
        self.shares_held = 0
        self.total_profit = 0

        # Features in state: Close price, sentiment, balance, shares held
        self.action_space = spaces.Discrete(3)  # 0 = Hold, 1 = Buy, 2 = Sell
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=(4,), dtype=np.float32
        )

    def reset(self):
        self.current_step = 0
        self.balance = 10000
        self.shares_held = 0
        self.total_profit = 0
        return self._get_obs()

    def _get_obs(self):
        row = self.df.iloc[self.current_step]
        return np.array([
            row['Close'],
            row.get('sentiment_score', 0),  # fallback if missing
            self.balance,
            self.shares_held
        ], dtype=np.float32)

    def step(self, action):
        row = self.df.iloc[self.current_step]
        current_price = row['Close']
        done = self.current_step == len(self.df) - 1
        reward = 0

        if action == 1:  # Buy
            if self.balance >= current_price:
                self.shares_held += 1
                self.balance -= current_price
        elif action == 2:  # Sell
            if self.shares_held > 0:
                self.balance += current_price
                profit = self.shares_held * current_price
                reward = profit
                self.total_profit += profit
                self.shares_held = 0

        self.current_step += 1
        return self._get_obs(), reward, done, {}

    def render(self):
        print(f"Step: {self.current_step}, Balance: {self.balance}, Shares: {self.shares_held}, Total Profit: {self.total_profit}")
