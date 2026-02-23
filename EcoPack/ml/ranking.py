import os
import pickle
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from dotenv import load_dotenv

# =========================
# 1️⃣ FIX PROJECT ROOT PATH
# =========================
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
MODEL_DIR = ROOT_DIR / "models"

print("MODEL DIRECTORY:", MODEL_DIR)

# =========================
# 2️⃣ LOAD ENV
# =========================
load_dotenv(ROOT_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set!")

engine = create_engine(DATABASE_URL)

# =========================
# 3️⃣ LOAD MODELS
# =========================
try:
    with open(MODEL_DIR / "rf_cost_model.pkl", "rb") as f:
        cost_model = pickle.load(f)

    with open(MODEL_DIR / "xgb_co2_model.pkl", "rb") as f:
        co2_model = pickle.load(f)

    with open(MODEL_DIR / "scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    print("✅ MODELS LOADED SUCCESSFULLY")

except Exception as e:
    print("❌ MODEL LOAD ERROR:", e)

# =========================
# 4️⃣ MATERIAL RANKING
# =========================
def get_material_ranking(
    product_type,
    product_category,
    fragility,
    shipping_type,
    sustainability_priority
):

    try:
        df = pd.read_sql(text("SELECT * FROM material"), engine)

        if df.empty:
            print("❌ MATERIAL TABLE EMPTY")
            return pd.DataFrame()

    except Exception as e:
        print("❌ DB ERROR:", e)
        return pd.DataFrame()

    features = [
        "strength",
        "weight_capacity",
        "biodegradability_score",
        "recyclability_percentage"
    ]

    X_raw = df[features]
    X_scaled = scaler.transform(X_raw)

    # ================= MODEL PREDICTIONS =================
    df["cost_rupees"] = cost_model.predict(X_raw)
    df["co2_score"] = co2_model.predict(X_scaled)

    # ================= FRAGILITY FILTER =================
    fragility = (fragility or "").lower()

    if fragility == "high":
        df = df[df["strength"] >= 3]
    elif fragility == "medium":
        df = df[df["strength"] >= 2]
    else:
        df = df[df["strength"] >= 1]

    if df.empty:
        return pd.DataFrame()

    # ================= CATEGORY SUITABILITY =================
    def material_priority_score(row):

        cat = (product_category or "").lower()

        if cat == "food":
            return 0.5 * row["biodegradability_score"] + 0.5 * row["recyclability_percentage"]

        elif cat == "electronics":
            return 0.6 * row["strength"] + 0.4 * row["weight_capacity"]

        else:
            return (
                0.4 * row["strength"] +
                0.3 * row["biodegradability_score"] +
                0.3 * row["recyclability_percentage"]
            )

    df["suitability_score"] = df.apply(material_priority_score, axis=1)

    # ================= NORMALIZATION =================
    df["cost_score"] = 1 - (
        (df["cost_rupees"] - df["cost_rupees"].min()) /
        (df["cost_rupees"].max() - df["cost_rupees"].min() + 1e-6)
    )

    df["co2_score_norm"] = 1 - (
        (df["co2_score"] - df["co2_score"].min()) /
        (df["co2_score"].max() - df["co2_score"].min() + 1e-6)
    )

    df["suitability_norm"] = (
        (df["suitability_score"] - df["suitability_score"].min()) /
        (df["suitability_score"].max() - df["suitability_score"].min() + 1e-6)
    )

    # ================= WEIGHTS =================
    cost_w, co2_w, suit_w = 0.4, 0.4, 0.2

    sustainability_priority = (sustainability_priority or "").lower()
    shipping_type = (shipping_type or "").lower()

    if sustainability_priority == "high":
        co2_w += 0.1
        suit_w += 0.05
        cost_w -= 0.15

    if shipping_type == "international":
        co2_w += 0.1
        cost_w -= 0.05

    total = cost_w + co2_w + suit_w
    cost_w /= total
    co2_w /= total
    suit_w /= total

    df["final_score"] = (
        cost_w * df["cost_score"] +
        co2_w * df["co2_score_norm"] +
        suit_w * df["suitability_norm"]
    )

    df = df.sort_values("final_score", ascending=False)
    df["rank"] = range(1, len(df) + 1)

    return df[[
        "material_name",
        "cost_rupees",
        "co2_score",
        "suitability_score",
        "final_score",
        "rank"
    ]]