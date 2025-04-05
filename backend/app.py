from flask import Flask, jsonify, request
from flask_cors import CORS
from database import init_db, insert_trade, get_trades
from trading_logic import generate_trade_signal

app = Flask(__name__)
CORS(app)  # Enable CORS
init_db()

@app.route('/api/signal', methods=['GET'])
def get_signal():
    signal = generate_trade_signal()
    return jsonify({'signal': signal})

@app.route('/api/trades', methods=['POST'])
def save_trade():
    data = request.json
    insert_trade(data['symbol'], data['action'], data['confidence'])
    return jsonify({'status': 'Trade saved'})

@app.route('/api/trades', methods=['GET'])
def list_trades():
    trades = get_trades()
    return jsonify(trades)

if __name__ == '__main__':
    app.run(debug=True)
