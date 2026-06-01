import os
import easyocr

# Initialize OCR reader
reader = easyocr.Reader(['en'])

# Folder containing extracted frames
frames_folder = "frames/reel1"

# Output folder and file
metadata_folder = "metadata/reel1"
output_file = os.path.join(metadata_folder, "ocr.txt")

# Create metadata folder if it doesn't exist
os.makedirs(metadata_folder, exist_ok=True)

# Store unique text
all_text = set()

# Loop through all frame images
for file in sorted(os.listdir(frames_folder)):
    if file.endswith(".jpg"):
        image_path = os.path.join(frames_folder, file)

        print(f"Reading: {file}")

        result = reader.readtext(image_path, detail=0)

        for text in result:
            cleaned = text.strip()

            if cleaned:
                all_text.add(cleaned)

# Save results
with open(output_file, "w", encoding="utf-8") as f:
    for text in sorted(all_text):
        f.write(text + "\n")

print(f"\nOCR data saved to: {output_file}")