# backend/app.py

import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import pandas as pd

# =========================
# Local Imports
# =========================
from ml.ranking import get_material_ranking
import analytics
from export_utils import export_pdf, export_excel

# =========================
# Load Environment
# =========================
BACKEND_DIR = Path(__file__).resolve().parent
env_path = BACKEND_DIR.parent / ".env"  # Assuming .env is at project root
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

# =========================
# Flask App
# =========================
app = Flask(
    __name__,
    template_folder=str(BACKEND_DIR.parent / "templates"),
    static_folder=str(BACKEND_DIR.parent / "static")
)

# =========================
# In-memory store
# =========================
LAST_RANKINGS = pd.DataFrame()

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
# MATERIAL RANKING API
# ==========================================================
@app.route("/api/ranking", methods=["POST"])
def ranking():
    global LAST_RANKINGS
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        df = get_material_ranking(
            product_type=data.get("product_type"),
            product_category=data.get("product_category"),
            fragility=data.get("fragility"),
            shipping_type=data.get("shipping_type"),
            sustainability_priority=data.get("sustainability_priority")
        )

        if df.empty:
            return jsonify({"ranking": [], "metrics": {}})

        df = df.head(5).copy()
        df["rank"] = range(1, len(df) + 1)

        numeric_cols = ["cost_rupees", "co2_score", "suitability_score", "final_score"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(float)

        LAST_RANKINGS = df.copy()
        analytics.LAST_RANKINGS = LAST_RANKINGS

        metrics = analytics.calculate_dashboard_metrics(df)

        return jsonify({
            "ranking": df.to_dict(orient="records"),
            "metrics": metrics
        })

    except Exception as e:
        print("Ranking API Error:", e)
        return jsonify({"error": str(e)}), 500

# ==========================================================
# DASHBOARD METRICS API
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

        metrics = analytics.calculate_dashboard_metrics(analytics.LAST_RANKINGS)
        return jsonify(metrics)

    except Exception as e:
        print("Dashboard Metrics Error:", e)
        return jsonify({"error": str(e)}), 500

# ==========================================================
# ANALYTICS / TRENDS API
# ==========================================================
@app.route("/api/trends", methods=["GET"])
def trends():
    try:
        comparison = analytics.get_top5_comparison_data()
        usage_trend = analytics.get_material_usage_trend()
        co2_trend = analytics.get_co2_trend()
        cost_trend = analytics.get_cost_trend()

        return jsonify({
            "comparison": comparison or [],
            "usage_trend": usage_trend or [],
            "co2_trend": co2_trend or [],
            "cost_trend": cost_trend or []
        })

    except Exception as e:
        print("Trends API Error:", e)
        return jsonify({"error": str(e)}), 500

# ==========================================================
# EXPORT PDF / EXCEL APIs
# ==========================================================
@app.route("/api/export/pdf", methods=["GET"])
def export_pdf_api():
    return export_pdf()

@app.route("/api/export/excel", methods=["GET"])
def export_excel_api():
    return export_excel()

# ==========================================================
# PRODUCTION RUN (Render uses gunicorn)
# ==========================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
