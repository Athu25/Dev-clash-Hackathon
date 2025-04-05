# backend/model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

from utils import create_target_label, get_features_and_labels


# 1. Load data
data_path = 'data/AAPL_data.csv'
data = pd.read_csv(data_path)
print(data.columns)
data.columns = data.columns.str.strip() 

# 2. Preprocess: Create target label
data = create_target_label(data)
data = data.dropna()  # Remove last row with NaN target


# 3. Prepare X and y
X, y = get_features_and_labels(data)

# 4. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# 7. Save model
model_dir = 'models'
os.makedirs(model_dir, exist_ok=True)
joblib.dump(model, os.path.join(model_dir, 'model.pkl'))
