import requests
import piexif
from PIL import Image
from io import BytesIO
import json

# Step 1: Download a sample image
url = "https://assets.rappler.com/A764505656AF400F8C0995C68EEA9E03/img/9782B72707254C758E6B9BA6DD8989C1/joy-belmonte-qc-mayor-oath-taking-june-30-2019-006_9782B72707254C758E6B9BA6DD8989C1.jpg"
print(f"Downloading sample image from {url}...")
response = requests.get(url)
img = Image.open(BytesIO(response.content))

# Step 2: Extract EXIF metadata
exif_data = img.info.get("exif")

if not exif_data:
    print("No EXIF data found in this image. Try another photo from a smartphone or camera.")
    output = {
        "Camera Make": None,
        "Camera Model": None,
        "Date/Time Original": None
    }
else:
    exif_dict = piexif.load(exif_data)

    # Step 3: Pull out interesting fields
    make = exif_dict["0th"].get(piexif.ImageIFD.Make, b"").decode(errors="ignore")
    model = exif_dict["0th"].get(piexif.ImageIFD.Model, b"").decode(errors="ignore")
    date_time = exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal, b"").decode(errors="ignore")

    print("\n=== EXIF Metadata Analysis ===")
    print("Camera Make:", make if make else "N/A")
    print("Camera Model:", model if model else "N/A")
    print("Date/Time Original:", date_time if date_time else "N/A")

    output = {
        "Camera Make": make if make else None,
        "Camera Model": model if model else None,
        "Date/Time Original": date_time if date_time else None
    }

# Step 4: Save to JSON file
with open("exif_output.json", "w") as f:
    json.dump(output, f, indent=4)

print("\nMetadata saved to exif_output.json")
