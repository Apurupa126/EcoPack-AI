# backend/ml/ranking.py

import os
import pickle
import pandas as pd
from sqlalchemy import create_engine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(BASE_DIR)
MODEL_DIR = os.path.join(BACKEND_DIR, "models")

# PostgreSQL connection
DB_URL = "postgresql://postgres:Apurupa@localhost:5432/ai"
engine = create_engine(DB_URL)

def get_material_ranking(
    product_type,
    product_category,
    fragility,
    shipping_type,
    sustainability_priority
):
    """
    Returns ranked materials with predicted cost, CO2 score, suitability, and final score.
    Works for all categories: Electronics, Food, Cosmetics.
    Fragility and sustainability priority now properly influence ranking.
    """

    # ---------------- LOAD MODELS ----------------
    with open(os.path.join(MODEL_DIR, "rf_cost_model.pkl"), "rb") as f:
        cost_model = pickle.load(f)
    with open(os.path.join(MODEL_DIR, "xgb_co2_model.pkl"), "rb") as f:
        co2_model = pickle.load(f)
    with open(os.path.join(MODEL_DIR, "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)

    # ---------------- LOAD DATA ----------------
    df = pd.read_sql("SELECT * FROM material", engine)

    features = ["strength", "weight_capacity", "biodegradability_score", "recyclability_percentage"]
    X_raw = df[features]
    X_scaled = scaler.transform(X_raw)

    # ---------------- PREDICTIONS ----------------
    df["cost_rupees"] = cost_model.predict(X_raw)
    df["co2_score"] = co2_model.predict(X_scaled)

    # ---------------- HARD FILTERS ----------------
    if fragility.lower() == "high":
        df = df[df["strength"] >= 3]
    elif fragility.lower() == "medium":
        df = df[df["strength"] >= 2]
    else:  # Low fragility
        df = df[df["strength"] >= 1]  # Avoid extremely weak materials

    if df.empty:
        # Return empty DataFrame if no materials pass the filters
        return pd.DataFrame(columns=[
            "material_name", "cost_rupees", "co2_score",
            "suitability_score", "final_score", "rank"
        ])

    # ---------------- NORMALIZATION ----------------
    df["cost_score"] = 1 - ((df["cost_rupees"] - df["cost_rupees"].min()) /
                            (df["cost_rupees"].max() - df["cost_rupees"].min() or 1))
    df["co2_score_norm"] = 1 - ((df["co2_score"] - df["co2_score"].min()) /
                                (df["co2_score"].max() - df["co2_score"].min() or 1))
    df["suitability_score"] = (0.4 * df["strength"] +
                               0.3 * df["recyclability_percentage"] +
                               0.3 * df["biodegradability_score"])
    df["suitability_norm"] = ((df["suitability_score"] - df["suitability_score"].min()) /
                              (df["suitability_score"].max() - df["suitability_score"].min() or 1))

    # ---------------- DYNAMIC WEIGHTS ----------------
    cost_w, co2_w, suit_w = 0.4, 0.4, 0.2

    # Adjust weights based on sustainability priority
    if sustainability_priority.lower() == "high":
        co2_w += 0.1
        suit_w += 0.05
        cost_w -= 0.15
    elif sustainability_priority.lower() == "low":
        co2_w -= 0.1
        suit_w -= 0.05
        cost_w += 0.15
    # Medium → keep default weights

    # Adjust weights for international shipping
    if shipping_type.lower() == "international":
        co2_w += 0.1
        cost_w -= 0.05

    # Normalize weights
    total = cost_w + co2_w + suit_w
    cost_w /= total
    co2_w /= total
    suit_w /= total

    # ---------------- FINAL SCORE ----------------
    df["final_score"] = (cost_w * df["cost_score"] +
                         co2_w * df["co2_score_norm"] +
                         suit_w * df["suitability_norm"])

    # ---------------- SORT & RANK ----------------
    df = df.sort_values("final_score", ascending=False)
    df["rank"] = range(1, len(df) + 1)

    # ---------------- RETURN ----------------
    return df[["material_name", "cost_rupees", "co2_score",
               "suitability_score", "final_score", "rank"]]
