🌱 **EcoPack-AI**

EcoPack-AI is an AI-powered Sustainable Packaging Recommendation System that helps businesses choose eco-friendly packaging materials by balancing cost, CO₂ emissions, and material suitability.

Built with Flask, Machine Learning, and PostgreSQL, EcoPack-AI provides dashboard analytics, exportable reports, and REST API endpoints.

Features

Intelligent Material Recommendation based on product category, fragility, shipping type, and sustainability priority

Predictive Models: Random Forest for cost prediction, XGBoost for CO₂ impact and ranking

Weighted Scoring System combining cost, CO₂, and strength for final ranking

Interactive Dashboard with top materials, trends, and historical analytics

Export Options: PDF and Excel report generation

REST API for integration with other applications

Project Structure
EcoPackAI/

├── backend/

│   ├── app.py                # Main Flask application & API endpoints

│   ├── data.py               # Database connection & data loading

│   ├── ml/

│   │   └── ranking.py        # Material ranking & ML logic

│   ├── analytics.py          # Dashboard metrics & trend calculations

│   ├── export_utils.py       # PDF/Excel export functions

│   ├── requirements.txt      # Python dependencies

│   └── .env                  # Environment variables (DATABASE_URL, API_KEY)

│

├── frontend/
│   ├── templates/            # HTML pages

│   │   ├── index.html


│   │   ├── intro.html

│   │   └── dashboard.html

│   └── static/               # CSS & JS

│       ├── css/style.css

│       └── js/main.js

│

├── render.yaml               # Render deployment configuration

├── Procfile                  # Render start command

└── README.md                 # Project documentation

How It Works

Users input product category, fragility, shipping type, and sustainability priority

Machine Learning models predict:

Random Forest for packaging cost

XGBoost for CO₂ footprint and material ranking

Weighted Ranking Logic:

Suitability Score = (Weco × CO2norm) + (Wcost × Costnorm) + (Wstrength × Strengthnorm)

Dashboard displays top materials, CO₂ and cost trends, and historical insights

Users can export reports as PDF or Excel

Tech Stack
Layer	Technology
Backend	Python, Flask, SQLAlchemy
Database	PostgreSQL
ML Models	Random Forest, XGBoost, Scikit-Learn, Pandas
Frontend	HTML, CSS, Bootstrap, JavaScript
Visualization	Plotly
Export	ReportLab (PDF), OpenPyXL (Excel)
Deployment	Gunicorn, Render
Installation & Setup

Clone the repository

git clone https://github.com/your-username/EcoPackAI.git
cd EcoPackAI/backend

Create Virtual Environment

# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate

Install Dependencies

pip install -r requirements.txt

Configure PostgreSQL

Create database: EcoPackAI

Import materials table

Update .env:

DATABASE_URL=postgresql://username:password@localhost:5432/EcoPackAI
API_KEY=your_api_key_here

Run the Application

python app.py

Access via: http://127.0.0.1:5000

API Endpoints
Endpoint	Method	Description
/	GET	Health check / Home page
/api/ranking	POST	Get top recommended materials
/api/dashboard-metrics	GET	Fetch dashboard metrics
/api/export/pdf	GET	Export recommendations as PDF
/api/export/excel	GET	Export recommendations as Excel
Machine Learning Details

Cost Prediction: Random Forest Regressor

CO₂ Prediction & Ranking: XGBoost

Input Features: CO₂ score, suitability, material properties

Evaluation Metrics: R², RMSE, MAE

Deployment (Render)

Build Command:

pip install -r backend/requirements.txt

Start Command:

gunicorn backend.app:app

Environment Variables:

DATABASE_URL

API_KEY

FLASK_ENV=production

Screenshots
