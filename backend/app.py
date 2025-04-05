from flask import Flask, jsonify
from flask_cors import CORS
from trading_logic import generate_trade_signal
from database import insert_trade, get_trades

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "✅ Backend running! Visit /api/signal or /api/trades."

@app.route('/api/signal', methods=['GET'])
def get_signal():
    signal = generate_trade_signal()
    insert_trade(signal['symbol'], signal['action'], signal['confidence'])
    return jsonify({'signal': signal})

@app.route('/api/trades', methods=['GET'])
def get_all_trades():
    trades = get_trades()
    return jsonify({'trades': trades})

if __name__ == '__main__':
    print("\n🔗 Available API Endpoints:")
    print("➡️  Home:           http://127.0.0.1:5000/")
    print("➡️  Get Signal:     http://127.0.0.1:5000/api/signal")
    print("➡️  Get All Trades: http://127.0.0.1:5000/api/trades\n")
    
    app.run(debug=True)
