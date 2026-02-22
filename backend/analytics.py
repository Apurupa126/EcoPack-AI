# backend/analytics.py

import pandas as pd

# ==========================================================
# Global in-memory rankings
# This will be updated from app.py after ranking API runs
# ==========================================================
LAST_RANKINGS = pd.DataFrame()


# ==========================================================
# 1️⃣ DASHBOARD METRICS
# ==========================================================
def calculate_dashboard_metrics(df):
    if df is None or df.empty:
        return {
            "avg_co2": 0,
            "avg_cost": 0,
            "avg_suitability": 0,
            "co2_reduction_percent": 0,
            "cost_savings_percent": 0
        }

    # Safe numeric conversion
    df["co2_score"] = pd.to_numeric(df.get("co2_score", 0), errors="coerce").fillna(0)
    df["cost_rupees"] = pd.to_numeric(df.get("cost_rupees", 0), errors="coerce").fillna(0)
    df["suitability_score"] = pd.to_numeric(df.get("suitability_score", 0), errors="coerce").fillna(0)

    avg_co2 = df["co2_score"].mean()
    avg_cost = df["cost_rupees"].mean()
    avg_suitability = df["suitability_score"].mean()

    # Baseline values (traditional packaging reference)
    traditional_co2 = 15
    traditional_cost = 10

    co2_reduction = ((traditional_co2 - avg_co2) / traditional_co2) * 100
    cost_savings = ((traditional_cost - avg_cost) / traditional_cost) * 100

    return {
        "avg_co2": round(float(avg_co2), 2),
        "avg_cost": round(float(avg_cost), 2),
        "avg_suitability": round(float(avg_suitability), 2),
        "co2_reduction_percent": round(float(co2_reduction), 2),
        "cost_savings_percent": round(float(cost_savings), 2)
    }


# ==========================================================
# 2️⃣ TOP 5 COMPARISON DATA
# ==========================================================
def get_top5_comparison_data():
    global LAST_RANKINGS

    if LAST_RANKINGS.empty:
        return []

    required_cols = ["material_name", "cost_rupees", "co2_score", "suitability_score"]
    existing_cols = [col for col in required_cols if col in LAST_RANKINGS.columns]

    if not existing_cols:
        return []

    return LAST_RANKINGS[existing_cols].to_dict(orient="records")


# ==========================================================
# 3️⃣ MATERIAL USAGE TREND
# ==========================================================
def get_material_usage_trend():
    global LAST_RANKINGS

    if LAST_RANKINGS.empty or "material_name" not in LAST_RANKINGS.columns:
        return []

    trend = LAST_RANKINGS["material_name"].value_counts().head(5)

    return [
        {"material_name": name, "count": int(count)}
        for name, count in trend.items()
    ]


# ==========================================================
# 4️⃣ CO2 TREND
# ==========================================================
def get_co2_trend():
    global LAST_RANKINGS

    if LAST_RANKINGS.empty:
        return []

    if "material_name" not in LAST_RANKINGS.columns or "co2_score" not in LAST_RANKINGS.columns:
        return []

    trend = (
        LAST_RANKINGS
        .groupby("material_name")["co2_score"]
        .mean()
        .reset_index()
    )

    trend = trend.rename(columns={"co2_score": "avg_co2"})

    return trend.to_dict(orient="records")


# ==========================================================
# 5️⃣ COST TREND
# ==========================================================
def get_cost_trend():
    global LAST_RANKINGS

    if LAST_RANKINGS.empty:
        return []

    if "material_name" not in LAST_RANKINGS.columns or "cost_rupees" not in LAST_RANKINGS.columns:
        return []

    trend = (
        LAST_RANKINGS
        .groupby("material_name")["cost_rupees"]
        .mean()
        .reset_index()
    )

    trend = trend.rename(columns={"cost_rupees": "avg_cost"})

    return trend.to_dict(orient="records")