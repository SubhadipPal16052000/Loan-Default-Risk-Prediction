import pandas as pd
import toml
from sqlalchemy import create_engine

# =========================
# LOAD SECRETS
# =========================

config = toml.load(".streamlit/secrets.toml")

DATABASE_URL = config["DATABASE_URL"]

# =========================
# LOAD CSV
# =========================

df = pd.read_csv("data/loan_data.csv")

# =========================
# CLEAN COLUMN NAMES
# =========================

df.columns = (
    df.columns
    .str.strip()
    .str.replace(".", "_", regex=False)
    .str.replace(" ", "_", regex=False)
    .str.lower()
)

print("Cleaned Columns:")
print(df.columns)

# =========================
# CREATE ENGINE
# =========================

engine = create_engine(DATABASE_URL)

# =========================
# UPLOAD TO NEON
# =========================

df.to_sql(
    "loan_data",
    engine,
    if_exists="replace",
    index=False
)

print("✅ Data uploaded successfully to Neon!")