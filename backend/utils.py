import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from backend.sentiment_analysis import get_sentiment_score

# For supervised ML (e.g., LSTM)
def get_features_and_labels(df):
    df = df.copy()
    if 'Date' in df.columns:
        df = df.drop(columns=['Date'])
    if 'Target' not in df.columns:
        raise ValueError("Target column not found in the DataFrame.")

    X = df.drop('Target', axis=1)
    y = df['Target']
    return X, y

# For RL/time-series forecasting
def preprocess_data_for_rl(df, sequence_length=30):
    df = df.sort_values("Date")
    df = df.dropna()

    features = ['Open', 'High', 'Low', 'Close', 'Volume']
    df_filtered = df[features]

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df_filtered)

    sequences = []
    for i in range(len(scaled_data) - sequence_length):
        sequences.append(scaled_data[i:i + sequence_length])

    X = np.array(sequences)
    return X, scaler

# For generating labels (binary classification)
def create_target_label(df):
    df = df.copy()
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    return df.dropna()

# Add sentiment per-date
def add_sentiment_feature(df, stock_symbol='AAPL'):
    df = df.copy()
    if 'Date' not in df.columns:
        raise ValueError("Expected 'Date' column for adding sentiment feature.")
    df['Date'] = pd.to_datetime(df['Date'])
    df['sentiment_score'] = df['Date'].apply(lambda d: get_sentiment_score(stock_symbol, date=d.date()))
    return df
