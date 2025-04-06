from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from trading_logic import generate_trade_signal
from database import insert_trade, get_trades
from dotenv import load_dotenv
import os
from alpaca_trade_api.rest import REST

# RL Imports
import pandas as pd
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from stock_trading_env import StockTradingEnv
from tensorflow.keras.models import load_model
import joblib

# Load environment variables
load_dotenv()

# Alpaca API setup
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL")
alpaca = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL)

# Flask setup
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ Backend running!"

@app.route("/api/signal", methods=["GET"])
def get_signal():
    symbol = request.args.get("symbol", "AAPL")
    signal = generate_trade_signal(symbol)
    insert_trade(symbol, signal["action"], signal["confidence"])
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
    duration = data.get("duration", "day")

    signal = generate_trade_signal(symbol)
    action = signal["action"]

    if action == "hold":
        return jsonify({"message": "📉 No trade executed (hold signal)", "signal": signal}), 200

    try:
        order = alpaca.submit_order(
            symbol=symbol,
            qty=qty,
            side=action,
            type="market",
            time_in_force=duration
        )
        insert_trade(symbol, action, signal["confidence"])
        return jsonify({
            "message": f"✅ {action.upper()} order executed!",
            "signal": signal,
            "order": order._raw
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/run-rl-agent", methods=["POST"])
def run_rl_agent():
    data = request.json
    symbol = data.get("symbol", "AAPL")
    csv_path = f"data/{symbol}_data.csv"

    try:
        df = pd.read_csv(csv_path)

        # Load models
        lstm_model = load_model("models/lstm_model_fixed.h5")
        scaler = joblib.load("models/scaler.pkl")

        def create_lstm_features(df, time_steps=60):
            features = df.drop(columns=['Date'])
            features_scaled = scaler.transform(features)
            return np.array([features_scaled[i:i+time_steps] for i in range(len(features_scaled) - time_steps)])

        def add_lstm_signals(df):
            df = df.copy()
            X_seq = create_lstm_features(df)
            predictions = lstm_model.predict(X_seq).squeeze()
            lstm_signals = np.concatenate([np.zeros(len(df) - len(predictions)), predictions])
            df['lstm_signal'] = lstm_signals
            return df

        enhanced_df = add_lstm_signals(df)
        env = DummyVecEnv([lambda: StockTradingEnv(enhanced_df)])
        model = DQN.load("models/rl_trading_model")

        obs = env.reset()
        done = False
        trade_log = []

        while not done:
            action, _ = model.predict(obs)
            obs, reward, done, info = env.step(action)
            step = env.get_attr("current_step")[0]
            trade_log.append({
                "step": step,
                "action": int(action),
                "reward": float(reward)
            })

        return jsonify({"status": "success", "trades": trade_log})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/trades-ui")
def trade_logs_ui():
    return render_template("index.html")

if __name__ == "__main__":
    print("\n🔗 Available API Endpoints:")
    print("➡️  Home:               http://127.0.0.1:5000/")
    print("➡️  Get Signal:         http://127.0.0.1:5000/api/signal?symbol=AAPL")
    print("➡️  Get All Trades:     http://127.0.0.1:5000/api/trades")
    print("➡️  Execute Trade:      http://127.0.0.1:5000/api/execute-trade")
    print("➡️  Run RL Agent:       http://127.0.0.1:5000/api/run-rl-agent")
    print("➡️  Trade Logs UI:      http://127.0.0.1:5000/trades-ui\n")
    app.run(debug=True)
