import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.utils import (
    get_features_and_labels,
    create_target_label,
    add_sentiment_feature,
    add_technical_indicators
)

# Load and preprocess the data
data = pd.read_csv("data/AAPL_data.csv")

# Step 1: Create target label
data = create_target_label(data)

# Step 2: Add sentiment score as a new feature
data = add_sentiment_feature(data, stock_symbol='AAPL')

data = add_technical_indicators(data)

# Step 3: Get features and labels
X_raw, y = get_features_and_labels(data)

# Step 4: Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw)

# Step 5: Create LSTM sequences
def create_sequences(X, y, time_steps=90):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X[i:i + time_steps]
        Xs.append(v)
        ys.append(y[i + time_steps])
    return np.array(Xs), np.array(ys)

X_seq, y_seq = create_sequences(X_scaled, y.values)

# Step 6: Split into training and testing
split = int(0.8 * len(X_seq))
X_train, X_test = X_seq[:split], X_seq[split:]
y_train, y_test = y_seq[:split], y_seq[split:]

# Step 7: Build the LSTM model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization

# Build deeper LSTM model
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.3))
model.add(BatchNormalization())

model.add(LSTM(64, return_sequences=True))
model.add(Dropout(0.3))
model.add(BatchNormalization())

model.add(LSTM(32, return_sequences=False))
model.add(Dropout(0.3))

model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))  # Binary classification

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Step 8: Train the model
model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=64,
    validation_split=0.1,
    callbacks=[EarlyStopping(monitor='val_loss', patience=5)],
    verbose=1
)

# Step 9: Evaluate and print test accuracy
loss, accuracy = model.evaluate(X_test, y_test)
print(f"✅ Test Accuracy: {accuracy:.4f}")

loss, accuracy = model.evaluate(X_train, y_train)
print(f"✅ Train Accuracy: {accuracy:.4f}")

# Step 10: Save model and scaler
os.makedirs("models", exist_ok=True)
model.save("models/lstm_model.h5")
joblib.dump(scaler, "models/scaler.pkl")

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Make predictions
y_pred = model.predict(X_test)
y_pred_classes = (y_pred > 0.5).astype(int).reshape(-1)

# Accuracy
acc = accuracy_score(y_test, y_pred_classes)
print(f"\n✅ Model Accuracy on Test Data: {acc:.4f}")

# Detailed classification report
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred_classes))

