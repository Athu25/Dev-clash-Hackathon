import os
from dotenv import load_dotenv
from alpaca_trade_api.rest import REST

# Load credentials from .env
load_dotenv()

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL")

# Create Alpaca client
alpaca = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL)

# Get historical daily stock data (e.g., last 30 days)
def get_stock_data(symbol):
    bars = alpaca.get_bars(symbol, timeframe="1Day", limit=30).df
    bars = bars.reset_index()
    return bars
