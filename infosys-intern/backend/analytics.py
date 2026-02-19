# ======================================================
# analytics.py
# ======================================================

import pandas as pd
from data import engine


# ======================================================
# 1️⃣ DASHBOARD METRICS
# ======================================================
def calculate_dashboard_metrics(df):

    if df.empty:
        return {
            "avg_co2": 0,
            "avg_cost": 0,
            "avg_suitability": 0,
            "co2_reduction_percent": 0,
            "cost_savings_percent": 0
        }

    avg_co2 = df["co2_score"].mean()
    avg_cost = df["cost_rupees"].mean()
    avg_suitability = df["suitability_score"].mean()

    # Baseline values (traditional packaging)
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


# ======================================================
# 2️⃣ TOP 5 COMPARISON DATA
# (Used in Cost, CO2, Suitability charts)
# ======================================================
def get_top5_comparison_data():
    try:
        df = pd.read_sql(
            """
            SELECT material_name, cost_rupees, co2_score, suitability_score
            FROM prediction_history
            ORDER BY id DESC
            LIMIT 5
            """,
            engine
        )

        if df.empty:
            return []

        return df.to_dict(orient="records")

    except Exception as e:
        print("Comparison Error:", e)
        return []


# ======================================================
# 3️⃣ MATERIAL USAGE TREND
# ======================================================
def get_material_usage_trend():
    try:
        df = pd.read_sql(
            """
            SELECT material_name, COUNT(*) as count
            FROM prediction_history
            GROUP BY material_name
            ORDER BY count DESC
            LIMIT 5
            """,
            engine
        )

        if df.empty:
            return []

        return df.to_dict(orient="records")

    except Exception as e:
        print("Usage Trend Error:", e)
        return []


# ======================================================
# 4️⃣ CO2 TREND (Average per material)
# ======================================================
def get_co2_trend():
    try:
        df = pd.read_sql(
            """
            SELECT material_name, AVG(co2_score) as avg_co2
            FROM prediction_history
            GROUP BY material_name
            """,
            engine
        )

        if df.empty:
            return []

        return df.to_dict(orient="records")

    except Exception as e:
        print("CO2 Trend Error:", e)
        return []


# ======================================================
# 5️⃣ COST TREND (Average per material)
# ======================================================
def get_cost_trend():
    try:
        df = pd.read_sql(
            """
            SELECT material_name, AVG(cost_rupees) as avg_cost
            FROM prediction_history
            GROUP BY material_name
            """,
            engine
        )

        if df.empty:
            return []

        return df.to_dict(orient="records")

    except Exception as e:
        print("Cost Trend Error:", e)
        return []
