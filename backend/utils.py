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
