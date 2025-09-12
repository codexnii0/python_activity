# entity_extractor.py

import pandas as pd
import spacy

# 1. Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

# 2. Load the CSV file from Week 4
df = pd.read_csv("anomalies_detected_evidence.csv")

# 3. Create a list to hold extracted entities
entities_data = []

# 4. Process each row in the "message" column
for i, message in enumerate(df["message"], start=1):
    if pd.isna(message):
        continue  # skip empty values
    
    doc = nlp(str(message))  # process text with SpaCy
    
    for ent in doc.ents:  # iterate over detected entities
        entities_data.append({
            "row_id": i,          # which row it came from
            "entity_text": ent.text,
            "entity_label": ent.label_
        })

# 5. Save results to new CSV file
entities_df = pd.DataFrame(entities_data)
entities_df.to_csv("extracted_entities.csv", index=False)

print("✅ Entity extraction complete. Results saved to extracted_entities.csv")
