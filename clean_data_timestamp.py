import pandas as pd
import os
 
# File paths
cleaned_data_path = 'cleaned_evidence.csv'
feature_engineered_path = 'feature_engineered_evidence.csv'

# Check if raw data exists
if not os.path.exists(cleaned_data_path):
    print(f"❌ Error: '{cleaned_data_path}' not found. Please complete Week 1 activity first.")
    exit()
 
# Load raw data
df = pd.read_csv(cleaned_data_path)
 
# Handle missing values
df.fillna('UNKNOWN', inplace=True)
 
# Convert timestamp column to datetime objects
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Filtered timestamp
df['hour_of_day'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.day_of_week
df['is_weekend'] = df['day_of_week'].isin(['Saturday','Sunday'])
 
# Save cleaned data
df.to_csv(feature_engineered_path, index=False)
print(f"✅ Successfully cleaned and saved data to '{cleaned_data_path}'.")
 
# Show first 5 rows of cleaned data
print("\nFirst 5 rows of cleaned data:")
print(df.head())