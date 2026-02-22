# backend/ml/train_model.py

import sys
import os
from pathlib import Path
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# ============================
# 1. Fix module path
# ============================
# Add parent directory (backend/) to sys.path so we can import data.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data import load_material_data  # data.py must have Render Postgres connection

# ============================
# 2. Load dataset
# ============================
df = load_material_data()
print("Dataset shape:", df.shape)
print(df.head())

# ============================
# 3. Define features & targets
# ============================
X = df[[
    "strength",
    "weight_capacity",
    "biodegradability_score",
    "recyclability_percentage"
]]

y_cost_rupees = df["cost_rupees"]
y_co2_score = df["co2_score"]

# ============================
# 4. Train-Test Split
# ============================
X_train, X_test, y_cost_train, y_cost_test, y_co2_train, y_co2_test = train_test_split(
    X,
    y_cost_rupees,
    y_co2_score,
    test_size=0.2,
    random_state=42
)

# ============================
# 5. Feature Scaling (for XGBoost)
# ============================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler
os.makedirs("../models", exist_ok=True)
with open("../models/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
print("Scaler saved successfully")

# ============================
# 6. Random Forest – COST Prediction
# ============================
rf_cost_model = RandomForestRegressor(
    n_estimators=400,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)

rf_cost_model.fit(X_train, y_cost_train)
y_cost_pred = rf_cost_model.predict(X_test)

# Save model
with open("../models/rf_cost_model.pkl", "wb") as f:
    pickle.dump(rf_cost_model, f)

# Regression metrics
mae_cost = mean_absolute_error(y_cost_test, y_cost_pred)
rmse_cost = np.sqrt(mean_squared_error(y_cost_test, y_cost_pred))
r2_cost = r2_score(y_cost_test, y_cost_pred)

print("\n===== COST PREDICTION (Random Forest) =====")
print("MAE :", mae_cost)
print("RMSE:", rmse_cost)
print("R2  :", r2_cost)

# ============================
# 7. XGBoost – CO2 Prediction
# ============================
xgb_co2_model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.1,
    random_state=42
)

xgb_co2_model.fit(X_train_scaled, y_co2_train)
y_co2_pred = xgb_co2_model.predict(X_test_scaled)

# Save model
with open("../models/xgb_co2_model.pkl", "wb") as f:
    pickle.dump(xgb_co2_model, f)

# Regression metrics
mae_co2 = mean_absolute_error(y_co2_test, y_co2_pred)
rmse_co2 = np.sqrt(mean_squared_error(y_co2_test, y_co2_pred))
r2_co2 = r2_score(y_co2_test, y_co2_pred)

print("\n===== CO₂ PREDICTION (XGBoost) =====")
print("MAE :", mae_co2)
print("RMSE:", rmse_co2)
print("R2  :", r2_co2)

# ============================
# 8. Classification Metrics (for analysis)
# ============================
# COST
cost_threshold = y_cost_test.median()
y_cost_true_cls = (y_cost_test >= cost_threshold).astype(int)
y_cost_pred_cls = (y_cost_pred >= cost_threshold).astype(int)

print("\n===== COST CLASSIFICATION METRICS =====")
print("Accuracy :", accuracy_score(y_cost_true_cls, y_cost_pred_cls))
print("Precision:", precision_score(y_cost_true_cls, y_cost_pred_cls))
print("Recall   :", recall_score(y_cost_true_cls, y_cost_pred_cls))
print("F1-score :", f1_score(y_cost_true_cls, y_cost_pred_cls))

# CO2
co2_threshold = y_co2_test.median()
y_co2_true_cls = (y_co2_test >= co2_threshold).astype(int)
y_co2_pred_cls = (y_co2_pred >= co2_threshold).astype(int)

print("\n===== CO₂ CLASSIFICATION METRICS =====")
print("Accuracy :", accuracy_score(y_co2_true_cls, y_co2_pred_cls))
print("Precision:", precision_score(y_co2_true_cls, y_co2_pred_cls))
print("Recall   :", recall_score(y_co2_true_cls, y_co2_pred_cls))
print("F1-score :", f1_score(y_co2_true_cls, y_co2_pred_cls))

print("\n✅ TRAINING COMPLETED SUCCESSFULLY")