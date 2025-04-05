import random

def generate_trade_signal():
    actions = ["BUY", "SELL", "HOLD"]
    signal = {
        "symbol": "AAPL",
        "action": random.choice(actions),
        "confidence": round(random.uniform(0.5, 1.0), 2)
    }
    return signal
