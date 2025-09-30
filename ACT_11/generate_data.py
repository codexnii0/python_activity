# generate_data.py
"""
Generates a simulated raw evidence dataset for the final project.
Output: final_project_raw_data.csv
"""

import pandas as pd
import numpy as np
import uuid
import random
from datetime import datetime, timedelta

# --- Parameters ---
num_records = 100
artifact_types = ["image", "browser_history", "system_log", "registry", "pcap"]

# Helper function to random timestamp
def random_timestamp(start, end):
    delta = end - start
    rand_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=rand_seconds)

# Date range
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 3, 1)

# Simulate records
data = []
for _ in range(num_records):
    record = {
        "evidence_id": str(uuid.uuid4()),
        "acquired_at": random_timestamp(start_date, end_date).strftime("%Y-%m-%d %H:%M:%S"),
        "device_id": f"DEVICE-{random.randint(1,5)}",
        "source_path": f"/path/to/artifact_{random.randint(100,999)}.dat",
        "artifact_type": random.choice(artifact_types),
        "hash_md5": uuid.uuid4().hex[:16],  # fake hash
        "raw_payload_base64": None if random.random() < 0.3 else "c29tZSByYXcgZGF0YQ==",  # sometimes missing
    }
    data.append(record)

# Convert to DataFrame
df = pd.DataFrame(data)

# Save raw dataset
df.to_csv("final_project_raw_data.csv", index=False)
print("Generated final_project_raw_data.csv with", len(df), "records.")

