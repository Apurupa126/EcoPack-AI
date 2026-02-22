🌱 **EcoPackAI – AI-Powered Sustainable Packaging Recommendation System**

EcoPack-AI is an AI-powered Sustainable Packaging Recommendation System that helps businesses select eco-friendly packaging materials by optimizing cost, CO₂ emissions, and material suitability. It provides intelligent recommendations, predictive analytics, and exportable reports to support data-driven sustainable packaging decisions.

**Problem Statement**

Traditional packaging often relies on non-biodegradable materials, leading to:

- Environmental pollution and long-term ecological damage  
- High packaging costs due to inefficient material selection  
- Lack of intelligent decision-support systems for sustainable alternatives  

**Challenges faced by manual material selection:**

- **Environmental Impact:** Plastics and conventional materials harm ecosystems  
- **Cost Constraints:** Eco-friendly materials can be more expensive  
- **Fragility & Product Safety:** Some sustainable materials lack sufficient strength  
- **Material Availability & Standardization:** Limited availability and specifications  
- **CO₂ & Lifecycle Assessment:** Complex and data-intensive to calculate  
- **Consumer Preferences:** Not always aligned with sustainability  

**Solution Overview**

EcoPack-AI is a full-stack AI platform that:

- Collects eco-friendly packaging material data and stores it in PostgreSQL  
- Calculates sustainability metrics such as CO₂ impact and cost efficiency  
- Uses Random Forest to predict packaging cost  
- Uses XGBoost to predict CO₂ emissions and rank materials  
- Provides a Flask backend to process user inputs and generate recommendations  
- Displays results in a user-friendly frontend with dashboards and export options  

**Key Features**

- **AI-Based Packaging Recommendations:** Top 3 eco-friendly materials per product input  
- **CO₂ and Cost Prediction:** Enables sustainable and cost-effective decisions  
- **Interactive Reports & Analytics:** PDF/Excel reports with CO₂, cost, and suitability comparisons  
- **Weighted Scoring System:** Combines CO₂, cost, and strength for final ranking  
- **REST API:** Integrate EcoPack-AI with other services or applications  

**Technologies Used**

- **Backend:** Python, Flask  
- **Database:** PostgreSQL with SQLAlchemy  
- **Machine Learning:** Random Forest, XGBoost, Scikit-Learn  
- **Data Manipulation:** Pandas, NumPy  
- **Visualization:** Matplotlib, Plotly  
- **Frontend:** HTML, CSS, Bootstrap  
- **Deployment:** Render, Heroku  
- **Export:** ReportLab (PDF), OpenPyXL (Excel)  

**System Architecture**

- **User Interface Layer:** Collects product inputs (category, fragility, shipping type, sustainability priority)  
- **Application Layer:** Flask backend processes inputs and calls ML models  
- **Machine Learning Layer:** Predicts cost and CO₂ emissions; ranks materials  
- **Database Layer:** Stores eco-friendly material dataset and recommendation history  
- **Analytics & Output Layer:** Displays top 3 recommended materials, CO₂/cost comparisons, dashboards, and exportable reports  

**Dataset Overview**

- **Columns:** Material ID, Name, Strength, Weight Capacity, Cost, Biodegradability Score, CO₂ Score, Recyclability Percentage  
- **Data preprocessing:** handled missing values, normalized numeric features, encoded categorical variables  

**Machine Learning Models**

- **Random Forest:** Predicts packaging cost  
- **XGBoost:** Predicts CO₂ emissions  
- **Evaluation Metrics:** RMSE, MAE, R² Score  
- **Data Split:** Training and testing sets for reliable evaluation  

**Ranking Logic**

- Features normalized and weighted by sustainability priorities  
- Final ranking considers predicted cost, CO₂ emission, and material suitability  

**Dashboard Features**

- Top 5 recommended materials per product input  
- CO₂ and cost comparison graphs  
- Material performance trends  
- Exportable PDF and Excel reports  
- Insights for cost reduction and sustainability optimization  

**Future Scope**

- Integrate real-time shipping & logistics data to optimize CO₂ and cost dynamically  
- Enhanced dashboard analytics with trend predictions  
- Expand database with new materials and categories  

**Project Structure**


EcoPackAI/

├── backend/

│ ├── app.py # Flask app & API endpoints

│ ├── data.py # Database connection & data loading

│ ├── ml/

│ │ └── ranking.py # ML models & material ranking logic

│ ├── analytics.py # Dashboard metrics & trends

│ ├── export_utils.py # PDF & Excel export functions

│ ├── requirements.txt # Python dependencies

│ └── .env # Environment variables

├── frontend/

│ ├── templates/ # HTML pages

│ │ ├── index.html

│ │ ├── intro.html

│ │ └── dashboard.html

│ └── static/ # CSS & JS files

│ ├── css/style.css

│ └── js/main.js

├── render.yaml # Render deployment configuration

├── Procfile # Start command for Render deployment

└── README.md # Project documentation


**Installation & Setup**

1. **Clone the repository**
```bash
git clone https://github.com/your-username/EcoPack-AI.git
cd EcoPack-AI/backend

Create virtual environment

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Setup PostgreSQL

Create database: EcoPackAI

Import materials dataset

Update .env with DATABASE_URL and API_KEY

Run application

python app.py

Access at: http://127.0.0.1:5000

API Endpoints

Health Check: GET /

Get Recommendations: POST /api/ranking

Dashboard Metrics: GET /api/dashboard-metrics

Export PDF: GET /api/export/pdf

Export Excel: GET /api/export/excel
