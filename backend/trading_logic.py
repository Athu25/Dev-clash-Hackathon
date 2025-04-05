import random

# TODO: Replace this with actual ML model + Alpaca logic
def generate_trade_signal():
    # Simulate ML output
    choices = ['BUY', 'SELL', 'HOLD']
    action = random.choice(choices)
    confidence = round(random.uniform(0.6, 0.99), 2)
    return {
        'symbol': 'AAPL',
        'action': action,
        'confidence': confidence
    }
