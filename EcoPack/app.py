import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import pandas as pd

# =========================
# LOAD ENV FROM ROOT
# =========================
ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")

# =========================
# LOCAL IMPORTS
# =========================
from ml.ranking import get_material_ranking
import analytics
from export_utils import export_pdf, export_excel

# =========================
# FLASK APP
# =========================
app = Flask(__name__)

# =========================
# MEMORY STORE
# =========================
LAST_RANKINGS = pd.DataFrame()
analytics.LAST_RANKINGS = LAST_RANKINGS

# ==========================================================
# ROUTES
# ==========================================================
@app.route("/")
def intro():
    return render_template("intro.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ==========================================================
# RANKING API
# ==========================================================
@app.route("/api/ranking", methods=["POST"])
def ranking():
    global LAST_RANKINGS

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No input"}), 400

        ranking_df = get_material_ranking(
            product_type=data.get("product_type"),
            product_category=data.get("product_category"),
            fragility=data.get("fragility"),
            shipping_type=data.get("shipping_type"),
            sustainability_priority=data.get("sustainability_priority")
        )

        if ranking_df is None or ranking_df.empty:
            LAST_RANKINGS = pd.DataFrame()
            analytics.LAST_RANKINGS = LAST_RANKINGS
            return jsonify({"ranking": [], "metrics": {}})

        df = ranking_df.head(5).copy()
        df["rank"] = range(1, len(df) + 1)

        for col in [
            "cost_rupees",
            "co2_score",
            "suitability_score",
            "final_score"
        ]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        LAST_RANKINGS = df.copy()
        analytics.LAST_RANKINGS = LAST_RANKINGS

        metrics = analytics.calculate_dashboard_metrics(df)

        return jsonify({
            "ranking": df.to_dict(orient="records"),
            "metrics": metrics
        })

    except Exception as e:
        print("❌ RANKING ERROR:", e)
        return jsonify({"error": str(e)}), 500

# ==========================================================
# DASHBOARD METRICS
# ==========================================================
@app.route("/api/dashboard-metrics", methods=["GET"])
def dashboard_metrics():
    try:
        if analytics.LAST_RANKINGS.empty:
            return jsonify({
                "avg_co2": 0,
                "avg_cost": 0,
                "avg_suitability": 0,
                "co2_reduction_percent": 0,
                "cost_savings_percent": 0
            })

        metrics = analytics.calculate_dashboard_metrics(
            analytics.LAST_RANKINGS
        )

        return jsonify(metrics)

    except Exception as e:
        print("❌ DASHBOARD ERROR:", e)
        return jsonify({"error": str(e)}), 500

# ==========================================================
# TRENDS
# ==========================================================
@app.route("/api/trends", methods=["GET"])
def trends():
    try:
        if analytics.LAST_RANKINGS.empty:
            return jsonify({
                "comparison": [],
                "usage_trend": [],
                "co2_trend": [],
                "cost_trend": []
            })

        return jsonify({
            "comparison": analytics.get_top5_comparison_data(),
            "usage_trend": analytics.get_material_usage_trend(),
            "co2_trend": analytics.get_co2_trend(),
            "cost_trend": analytics.get_cost_trend()
        })

    except Exception as e:
        print("❌ TREND ERROR:", e)
        return jsonify({"error": str(e)}), 500

# ==========================================================
# EXPORT
# ==========================================================
@app.route("/api/export/pdf")
def export_pdf_api():
    if analytics.LAST_RANKINGS.empty:
        return jsonify({"error": "No ranking data"}), 400
    return export_pdf()

@app.route("/api/export/excel")
def export_excel_api():
    if analytics.LAST_RANKINGS.empty:
        return jsonify({"error": "No ranking data"}), 400
    return export_excel()

# ==========================================================
# RUN
# ==========================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)