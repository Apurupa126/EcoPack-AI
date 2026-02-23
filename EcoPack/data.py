import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load .env only for LOCAL development
load_dotenv()

# Works in BOTH Localhost + Render
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in environment variables")

# SQLAlchemy Engine
engine = create_engine(DATABASE_URL)

def load_material_data(table_name="material"):
    """
    Load material dataset from PostgreSQL.
    Returns a pandas DataFrame.
    """
    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(f"SELECT * FROM {table_name}"), conn)
        print("Dataset loaded successfully!")
        return df
    except Exception as e:
        print("DB Load Error:", e)
        return pd.DataFrame()