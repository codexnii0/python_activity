# anomaly_detector.py
# -------------------------------------------------------------
# This script loads the feature_engineered_evidence.csv dataset,
# applies Isolation Forest for anomaly detection, and creates
# anomalies_detected_evidence.csv with an additional "is_anomaly" column.
# -------------------------------------------------------------

import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def main():
    # Step 1: Load dataset
    input_file = "feature_engineered_evidence.csv"
    output_file = "anomalies_detected_evidence.csv"

    print(f"[INFO] Loading dataset: {input_file}")
    df_original = pd.read_csv(input_file)

    # Make a copy for feature engineering
    df = df_original.copy()

    # Step 2: Feature engineering
    # Convert boolean columns to int
    for col in df.select_dtypes(include=['bool']).columns:
        df[col] = df[col].astype(int)

    # Add keyword-based forensic flags from description (if present)
    if "description" in df_original.columns:
        df["flag_suspicious"] = df_original["description"].str.contains("suspicious", case=False, na=False).astype(int)
        df["flag_unknown"] = df_original["description"].str.contains("UNKNOWN", case=False, na=False).astype(int)
        df["flag_port_8080"] = df_original["description"].str.contains("8080", na=False).astype(int)
        df["flag_private_file"] = df_original["description"].str.contains("private_file", case=False, na=False).astype(int)

    # One-hot encode categoricals (example: event_type, user_id)
    categorical_cols = [col for col in ["event_type", "user_id"] if col in df.columns]
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Select numeric columns for modeling
    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.empty:
        raise ValueError("No numeric columns found for anomaly detection!")

    # Scale numeric data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_df)

    # Step 3: Apply Isolation Forest
    print("[INFO] Running Isolation Forest...")
    model = IsolationForest(
        n_estimators=200,   # number of trees
        contamination=0.45, # expected % of anomalies
        random_state=42
    )

    anomalies = model.fit_predict(scaled_data)

    # Step 4: Attach results to original dataset
    df_original["is_anomaly"] = anomalies

    # Save output file
    df_original.to_csv(output_file, index=False)
    print(f"[INFO] Anomalies flagged and saved to {output_file}")
    print("[INFO] -1 = anomaly, 1 = normal")
    print(df_original["is_anomaly"].value_counts())

if __name__ == "__main__":
    main()
