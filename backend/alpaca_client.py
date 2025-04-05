import os
from dotenv import load_dotenv
from alpaca_trade_api.rest import REST

load_dotenv()

api = REST(
    os.getenv("PKKN80C9APTWQD1Q361J"),
    os.getenv("sA8L7Z6xaFQ1Bgb5C7w6kRgksyyusq6NGUt0jYng "),
    base_url=os.getenv("https://paper-api.alpaca.markets/v2")
)

def get_live_price(symbol):
    barset = api.get_bars(symbol, timeframe="1Min", limit=1)
    return float(barset[-1].c) if barset else None
