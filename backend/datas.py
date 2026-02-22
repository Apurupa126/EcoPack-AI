import pandas as pd
import os

def load_materials():

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        csv_path = os.path.join(BASE_DIR, "ml", "material.csv")

        print("CSV PATH:", csv_path)

        df = pd.read_csv(csv_path)

        print("CSV Loaded Successfully")

        return df

    except Exception as e:

        print("CSV LOAD FAILED:", str(e))

        return None
