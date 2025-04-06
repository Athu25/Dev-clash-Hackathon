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

        # Action space: 0 = Hold, 1 = Buy, 2 = Sell
        self.action_space = spaces.Discrete(3)

        # Observation space: Close price, sentiment score, LSTM signal, balance, shares held
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=(5,), dtype=np.float32
        )

    def reset(self):
        self.current_step = 0
        self.balance = 10000
        self.shares_held = 0
        self.total_profit = 0
        return self._get_obs()

    def _get_obs(self):
        # Clamp to last valid index
        if self.current_step >= len(self.df):
            self.current_step = len(self.df) - 1

        row = self.df.iloc[self.current_step]

        return np.array([
            row['Close'],
            row.get('sentiment_score', 0),
            row.get('lstm_signal', 0),
            self.balance,
            self.shares_held
        ], dtype=np.float32)

    def step(self, action):
        row = self.df.iloc[self.current_step]
        current_price = row['Close']
        done = self.current_step >= len(self.df) - 1
        reward = 0

        # Buy
        if action == 1 and self.balance >= current_price:
            self.shares_held += 1
            self.balance -= current_price

        # Sell
        elif action == 2 and self.shares_held > 0:
            self.balance += current_price * self.shares_held
            reward = (current_price - self.df.iloc[self.current_step - 1]['Close']) * self.shares_held
            self.total_profit += reward
            self.shares_held = 0

        self.current_step += 1
        obs = self._get_obs()

        return obs, reward, done, {}

    def render(self, mode="human"):
        print(f"Step: {self.current_step}, Balance: {self.balance}, Shares: {self.shares_held}, Total Profit: {self.total_profit}")
