import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import StandardScaler
import joblib

# Load data
df = pd.read_csv("data/AAPL_data.csv")
df = df.drop(columns=["Date"])  # Drop 'Date' if it exists

# Preprocess
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)
joblib.dump(scaler, "models/scaler.pkl")

# Create sequences
def create_sequences(data, time_steps=60):
    X, y = [], []
    for i in range(time_steps, len(data)):
        X.append(data[i-time_steps:i])
        y.append(1 if data[i][3] > data[i-1][3] else 0)  # Index 3 = 'Close'
    return np.array(X), np.array(y)

X, y = create_sequences(scaled_data)

# Build model
model = Sequential()
model.add(LSTM(64, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(64))
model.add(Dropout(0.2))
model.add(Dense(1, activation="sigmoid"))

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
model.fit(X, y, epochs=5, batch_size=32)

# Save model in current TF/Keras format
model.save("models/lstm_model_fixed.h5")
print("✅ LSTM model retrained and saved as 'lstm_model_fixed.h5'")
