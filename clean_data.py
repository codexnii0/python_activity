import pandas as pd
import os
 
# File paths
raw_data_path = 'raw_evidence.csv'
cleaned_data_path = 'cleaned_evidence.csv'
 
# Check if raw data exists
if not os.path.exists(raw_data_path):
    print(f"❌ Error: '{raw_data_path}' not found. Please complete Week 1 activity first.")
    exit()
 
# Load raw data
df = pd.read_csv(raw_data_path)
 
# Handle missing values
df.fillna('UNKNOWN', inplace=True)
 
# Convert timestamp column to datetime objects
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
 
# Save cleaned data
df.to_csv(cleaned_data_path, index=False)
print(f"✅ Successfully cleaned and saved data to '{cleaned_data_path}'.")
 
# Show first 5 rows of cleaned data
print("\nFirst 5 rows of cleaned data:")
print(df.head())