# ==========================================================
# EcoPack AI - Main Flask Application
# ==========================================================

from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

# Local imports
from ml.ranking import get_material_ranking
from data import engine
from analytics import (
    calculate_dashboard_metrics,
    get_material_usage_trend,
    get_top5_comparison_data,
    get_co2_trend,
    get_cost_trend
)
from export_utils import export_pdf, export_excel

# ==========================================================
# APP CONFIGURATION
# ==========================================================

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

# ==========================================================
# INTRO PAGE
# ==========================================================

@app.route("/")
def intro():
    return render_template("intro.html")

# ==========================================================
# HOME PAGE (AI RECOMMENDATION PAGE)
# ==========================================================

@app.route("/home")
def home():
    return render_template("index.html")

# ==========================================================
# DASHBOARD PAGE
# ==========================================================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ==========================================================
# MATERIAL RANKING API
# ==========================================================

@app.route("/api/ranking", methods=["POST"])
def ranking():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # ==========================================
        # CALL ML MODEL
        # ==========================================
        df = get_material_ranking(
            product_type=data.get("product_type"),
            product_category=data.get("product_category"),
            fragility=data.get("fragility"),
            shipping_type=data.get("shipping_type"),
            sustainability_priority=data.get("sustainability_priority")
        )

        if df is None or df.empty:
            return jsonify({
                "ranking": [],
                "metrics": {}
            })

        # ==========================================
        # KEEP TOP 5 RESULTS
        # ==========================================
        df = df.head(5).copy()
        df["rank"] = range(1, len(df) + 1)

        # Convert numeric columns safely
        numeric_cols = ["cost_rupees", "co2_score", "suitability_score", "final_score"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(float)

        # ==========================================
        # SAVE TO DATABASE
        # ==========================================
        try:
            df.to_sql(
                "prediction_history",
                engine,
                if_exists="append",
                index=False
            )
        except Exception as db_error:
            print("Database Save Error:", db_error)

        # ==========================================
        # CALCULATE KPI METRICS
        # ==========================================
        metrics = calculate_dashboard_metrics(df)

        # ==========================================
        # RETURN RESPONSE
        # ==========================================
        return jsonify({
            "ranking": df.to_dict(orient="records"),
            "metrics": metrics
        })

    except Exception as e:
        print("Ranking API Error:", e)
        return jsonify({"error": str(e)}), 500

# ==========================================================
# DASHBOARD METRICS API (KPI CARDS)
# ==========================================================

@app.route("/api/dashboard-metrics", methods=["GET"])
def dashboard_metrics():
    try:
        df = pd.read_sql(
            """
            SELECT cost_rupees, co2_score, suitability_score
            FROM prediction_history
            ORDER BY id DESC
            LIMIT 5
            """,
            engine
        )

        if df.empty:
            return jsonify({
                "avg_co2": 0,
                "avg_cost": 0,
                "avg_suitability": 0,
                "co2_reduction_percent": 0,
                "cost_savings_percent": 0
            })

        metrics = calculate_dashboard_metrics(df)
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
        comparison = get_top5_comparison_data()
        usage_trend = get_material_usage_trend()
        co2_trend = get_co2_trend()
        cost_trend = get_cost_trend()

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
# EXPORT PDF API
# ==========================================================

@app.route("/api/export/pdf", methods=["GET"])
def export_pdf_api():
    try:
        return export_pdf()
    except Exception as e:
        print("PDF Export Error:", e)
        return jsonify({"error": str(e)}), 500

# ==========================================================
# EXPORT EXCEL API
# ==========================================================

@app.route("/api/export/excel", methods=["GET"])
def export_excel_api():
    try:
        return export_excel()
    except Exception as e:
        print("Excel Export Error:", e)
        return jsonify({"error": str(e)}), 500

# ==========================================================
# RUN APPLICATION (RENDER-READY)
# ==========================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
