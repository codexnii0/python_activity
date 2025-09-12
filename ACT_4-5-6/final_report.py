#!/usr/bin/env python3
"""
final_report.py

Generates a forensic report (forensic_report.md) and a visualization
(event_distribution.png) from:
 - anomalies_detected_evidence.csv
 - extracted_entities.csv

Usage:
    python final_report.py

Dependencies:
    pip install pandas matplotlib
"""

import os
import sys
from datetime import datetime
import textwrap

import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Configuration
# -----------------------------
ANOMALIES_CSV = "anomalies_detected_evidence.csv"
ENTITIES_CSV = "extracted_entities.csv"
OUTPUT_PNG = "event_distribution.png"
OUTPUT_MD = "forensic_report.md"

# -----------------------------
# Helper function: Load CSV safely
# -----------------------------
def load_csv(path):
    if not os.path.exists(path):
        print(f"ERROR: File not found: {path}")
        sys.exit(1)
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"ERROR: Failed to read {path}: {e}")
        sys.exit(1)

# -----------------------------
# Load data
# -----------------------------
print("Loading data...")
anom_df = load_csv(ANOMALIES_CSV)
ent_df = load_csv(ENTITIES_CSV)

# -----------------------------
# Schema summaries
# -----------------------------
def df_schema_summary(df):
    summary = []
    for col in df.columns:
        non_null = int(df[col].notnull().sum())
        dtype = str(df[col].dtype)
        summary.append((col, dtype, non_null))
    return summary

anom_schema = df_schema_summary(anom_df)
ent_schema = df_schema_summary(ent_df)

# -----------------------------
# Analysis: Event distribution
# -----------------------------
print("Analyzing event distribution...")

candidate_event_cols = [c for c in anom_df.columns if c.lower() in ("event", "event_type", "type", "action")]
event_col = candidate_event_cols[0] if candidate_event_cols else anom_df.columns[0]

event_counts = anom_df[event_col].fillna("<MISSING>").astype(str).value_counts()

# -----------------------------
# Analysis: Severity / Score
# -----------------------------
severity_col = None
for c in anom_df.columns:
    if c.lower() in ("severity", "score", "anomaly_score"):
        severity_col = c
        break

severity_summary = None
if severity_col is not None:
    scores = pd.to_numeric(anom_df[severity_col], errors="coerce")
    severity_summary = scores.describe()

# -----------------------------
# Analysis: Timeline
# -----------------------------
time_col = None
for c in anom_df.columns:
    if c.lower() in ("timestamp", "time", "datetime", "date"):
        time_col = c
        break

anom_by_time = None
if time_col is not None:
    try:
        anom_df["_parsed_time"] = pd.to_datetime(anom_df[time_col], errors="coerce")
        anom_by_time = anom_df.dropna(subset=["_parsed_time"]).set_index("_parsed_time").resample("D").size()
    except Exception:
        anom_by_time = None

# -----------------------------
# Analysis: Extracted Entities
# -----------------------------
print("Summarizing extracted entities...")

entity_col = None
for c in ent_df.columns:
    if c.lower() in ("entity", "value", "extracted", "text", "mention"):
        entity_col = c
        break
if entity_col is None:
    entity_col = ent_df.columns[0]

entity_counts = ent_df[entity_col].astype(str).fillna("<MISSING>").value_counts().head(20)

# -----------------------------
# Visualization: Event distribution
# -----------------------------
print(f"Creating visualization: {OUTPUT_PNG}")

plt.figure(figsize=(10, 6))
TOP_N = 12
event_counts.head(TOP_N).plot(kind="bar")
plt.title("Top Event Types (by Count)")
plt.ylabel("Count")
plt.xlabel(event_col)
plt.tight_layout()
plt.savefig(OUTPUT_PNG)
plt.close()

if anom_by_time is not None:
    timeline_png = "anomaly_timeline.png"
    print(f"Creating timeline visualization: {timeline_png}")
    plt.figure(figsize=(12, 4))
    anom_by_time.plot(kind="line", marker="o")
    plt.title("Anomalous Events Over Time (Daily)")
    plt.ylabel("Count")
    plt.xlabel("Date")
    plt.tight_layout()
    plt.savefig(timeline_png)
    plt.close()

# -----------------------------
# Markdown Report
# -----------------------------
print(f"Writing Markdown report: {OUTPUT_MD}")

now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

md_lines = []
md_lines.append("# Forensic Investigation Report\n")
md_lines.append(f"**Generated:** {now}\n")
md_lines.append("---\n")

# Executive Summary
md_lines.append("## Executive Summary\n")
md_lines.append("This report summarizes findings from a 5-week forensic investigation. The analyses combined anomaly detection outputs and entity extraction results to identify suspicious activity. Visualizations support the findings and make evidence easy to interpret.\n\n")

# Data Sources
md_lines.append("## Data Sources and Schema\n")
md_lines.append("- anomalies_detected_evidence.csv\n")
md_lines.append("- extracted_entities.csv\n\n")

md_lines.append("### anomalies_detected_evidence.csv (Schema Preview)\n")
for col, dtype, non_null in anom_schema:
    md_lines.append(f"- **{col}** — {dtype}, non-null: {non_null}\n")
md_lines.append("\n")

md_lines.append("### extracted_entities.csv (Schema Preview)\n")
for col, dtype, non_null in ent_schema:
    md_lines.append(f"- **{col}** — {dtype}, non-null: {non_null}\n")
md_lines.append("\n")

# Methodology
md_lines.append("## Methodology\n")
md_lines.append("The investigation followed a workflow: acquisition, preprocessing, feature engineering, anomaly detection, and entity extraction. Final synthesis aggregated anomaly outputs and entities, computed event distributions, and visualized trends.\n\n")

# Key Findings
md_lines.append("## Key Findings\n")

md_lines.append(f"### 1) Event Distribution (by `{event_col}`)\n")
for val, cnt in event_counts.head(12).items():
    md_lines.append(f"- **{val}** — {int(cnt)} occurrences\n")
md_lines.append(f"\n![Event distribution]({OUTPUT_PNG})\n\n")

if severity_summary is not None:
    md_lines.append(f"### 2) Anomaly Severity Summary (`{severity_col}`)\n")
    md_lines.append("````\n")
    md_lines.append(str(severity_summary))
    md_lines.append("\n````\n\n")

if anom_by_time is not None:
    md_lines.append("### 3) Timeline of Anomalous Events\n")
    md_lines.append("Daily aggregation highlights spikes that may indicate concentrated attack windows.\n\n")
    md_lines.append("![Anomaly timeline](anomaly_timeline.png)\n\n")

md_lines.append("### 4) Extracted Entities of Interest\n")
for val, cnt in entity_counts.items():
    md_lines.append(f"- **{val}** — {int(cnt)} mentions\n")
md_lines.append("\n")

# Recommendations
md_lines.append("## Recommendations\n")
md_lines.append("1. Investigate top event types and related entities.\n")
md_lines.append("2. Correlate anomalies with external logs and asset owners.\n")
md_lines.append("3. If severity is high, consider immediate containment (credential reset, isolation).\n")
md_lines.append("4. Preserve evidence and document chain-of-custody.\n\n")

# Appendix
md_lines.append("## Appendix\n")
md_lines.append("This report was auto-generated by final_report.py. Visualizations and Markdown are reproducible. For formal use, adjust script to explicit column names.\n")

with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print("Done. Outputs:")
print(f"- {OUTPUT_PNG}")
if anom_by_time is not None:
    print("- anomaly_timeline.png")
print(f"- {OUTPUT_MD}")
