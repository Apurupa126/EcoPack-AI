import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)

def load_material_data():
    query = "SELECT * FROM material"
    df = pd.read_sql(query, engine)
    return df
# data.py
