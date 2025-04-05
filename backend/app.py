from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from trading_logic import generate_trade_signal
from database import insert_trade, get_trades
from dotenv import load_dotenv
import os
from alpaca_trade_api.rest import REST

# Load environment variables
load_dotenv()

# Alpaca keys from .env
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL")

# Alpaca API client
alpaca = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL)

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ Backend running!"

@app.route("/api/signal", methods=["GET"])
def get_signal():
    symbol = request.args.get("symbol", "AAPL")
    signal = generate_trade_signal(symbol)
    insert_trade(signal["symbol"], signal["action"], signal["confidence"])
    return jsonify({"signal": signal})

@app.route("/api/trades", methods=["GET"])
def api_trades():
    trades = get_trades()
    return jsonify({"trades": trades})

@app.route("/api/execute-trade", methods=["POST"])
def execute_trade():
    data = request.json
    symbol = data.get("symbol")
    qty = int(data.get("quantity", 1))
    duration = data.get("duration", "day")  # Default: 'day'

    try:
        order = alpaca.submit_order(
            symbol=symbol,
            qty=qty,
            side="buy",        # you can make this dynamic later
            type="market",
            time_in_force=duration
        )
        return jsonify({"message": "✅ Trade executed!", "order": order._raw}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/trades-ui")
def trade_logs_ui():
    return render_template("index.html")

if __name__ == "__main__":
    print("\n🔗 Available API Endpoints:")
    print("➡️  Home:               http://127.0.0.1:5000/")
    print("➡️  Get Signal:         http://127.0.0.1:5000/api/signal?symbol=AAPL")
    print("➡️  Get All Trades:     http://127.0.0.1:5000/api/trades")
    print("➡️  Execute Trade:      http://127.0.0.1:5000/api/execute-trade")
    print("➡️  Trade Logs UI:      http://127.0.0.1:5000/trades-ui\n")
    app.run(debug=True)
