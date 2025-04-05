import pandas as pd
import joblib
import os

from utils import create_target_label, get_features_and_labels

# Load the trained model once
model_path = os.path.join('models', 'model.pkl')
model = joblib.load(model_path)

# Load the latest data sample
def generate_trade_signal():
    data_path = os.path.join('data', 'AAPL_data.csv')
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()
    
    # Preprocess
    df = create_target_label(df)
    df = df.dropna()
    
    # Use the last row for prediction
    X, _ = get_features_and_labels(df)
    latest_sample = X.iloc[[-1]]

    prediction = model.predict(latest_sample)[0]
    confidence = max(model.predict_proba(latest_sample)[0])

    action = "BUY" if prediction == 1 else "SELL"

    return {
        "symbol": "AAPL",
        "action": action,
        "confidence": round(confidence, 2)
    }
