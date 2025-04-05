def create_target_label(df):
    df = df.copy()
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    return df.dropna()

def get_features_and_labels(df):
    df = df.copy()

    # Drop Date column (case-insensitive)
    for col in df.columns:
        if col.lower() == 'date':
            df = df.drop(columns=[col])
            break

    if 'Target' not in df.columns:
        raise ValueError("Target column not found in the DataFrame.")

    X = df.drop('Target', axis=1)
    y = df['Target']
    return X, y

from backend.sentiment_analysis import get_sentiment_score

def add_sentiment_feature(df, stock_symbol='AAPL'):
    df = df.copy()
    if 'Date' not in df.columns:
        raise ValueError("Expected 'Date' column for adding sentiment feature.")
    df['Date'] = pd.to_datetime(df['Date'])
    df['sentiment_score'] = df['Date'].apply(lambda d: get_sentiment_score(stock_symbol, date=d.date()))
    return df

