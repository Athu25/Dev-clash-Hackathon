def preprocess_data(df, sequence_length=30):
    from sklearn.preprocessing import MinMaxScaler
    import numpy as np

    df = df.sort_values("Date")  # sort by date just in case
    df = df.dropna()

    # Select relevant features (you can customize this)
    features = ['Open', 'High', 'Low', 'Close', 'Volume']
    df_filtered = df[features]

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df_filtered)

    sequences = []
    for i in range(len(scaled_data) - sequence_length):
        sequences.append(scaled_data[i:i + sequence_length])

    X = np.array(sequences)
    return X, scaler
