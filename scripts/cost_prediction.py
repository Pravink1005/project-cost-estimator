import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Load the dataset
df = pd.read_csv("data/real_project_cost_data.csv")

# Define input features (X) and target variable (y)
X = df[["Labor Cost", "Material Cost", "Equipment Cost", "Miscellaneous Cost", "Duration"]]
y = df["Total Cost"]

# Split data into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Fine-Tuned XGBoost Model
model = XGBRegressor(
    n_estimators=200,        # Increased number of trees (default 100)
    learning_rate=0.05,      # Lower learning rate (default 0.1)
    max_depth=6,             # Slightly deeper trees (default 3)
    subsample=0.8,           # Use 80% of data per tree
    colsample_bytree=0.8,    # Use 80% of features per tree
    random_state=42
)

# Train the model
model.fit(X_train_scaled, y_train)

# Evaluate Model
y_pred = model.predict(X_test_scaled)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"✅ Fine-Tuned XGBoost Model trained successfully!")
print(f"📉 Mean Absolute Error (MAE): {mae:.2f}")
print(f"📈 R-squared Score: {r2:.4f}")

# Save the trained model and scaler
joblib.dump(model, "models/xgboost_cost_estimator.pkl")
joblib.dump(scaler, "models/scaler.pkl")

print("✅ Model and Scaler saved successfully!")
