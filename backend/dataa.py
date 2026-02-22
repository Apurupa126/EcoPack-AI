# backend/data.py
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# PostgreSQL URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL not found in .env")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

def load_material_data(table_name="material"):
    """
    Load material dataset from PostgreSQL.
    Returns a pandas DataFrame.
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(f"SELECT * FROM {table_name}"), conn)
    print("Dataset loaded successfully!")
    return df
