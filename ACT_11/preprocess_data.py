# preprocess_data.py
"""
Reads final_project_raw_data.csv, cleans and preprocesses the data,
and saves the output to final_project_cleaned_data.csv.
"""

import pandas as pd

# Load raw data
df = pd.read_csv("final_project_raw_data.csv")

# --- Data Cleaning ---

# 1. Handle missing values
df["raw_payload_base64"].fillna("MISSING", inplace=True)

# 2. Convert acquired_at to datetime
df["acquired_at"] = pd.to_datetime(df["acquired_at"], errors="coerce")

# Drop rows where acquired_at failed to parse
df = df.dropna(subset=["acquired_at"])

# 3. Feature engineering: extract date parts
df["year"] = df["acquired_at"].dt.year
df["month"] = df["acquired_at"].dt.month
df["day"] = df["acquired_at"].dt.day
df["hour"] = df["acquired_at"].dt.hour

# 4. Normalize text columns (lowercase for consistency)
df["artifact_type"] = df["artifact_type"].str.lower()
df["device_id"] = df["device_id"].str.upper()

# 5. Drop duplicates
df = df.drop_duplicates(subset=["evidence_id"])

# --- Save cleaned dataset ---
df.to_csv("final_project_cleaned_data.csv", index=False)
print("Saved cleaned data to final_project_cleaned_data.csv with", len(df), "records.")

