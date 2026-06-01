import re

input_file = "metadata/reel1/ocr.txt"
output_file = "metadata/reel1/cleaned_ocr.txt"

seen = set()
cleaned_lines = []

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    text = line.strip()

    # Skip empty lines
    if not text:
        continue

    # Rule 1: Minimum length
    if len(text) < 3:
        continue

    # Rule 2: Must contain at least one letter
    if not re.search(r"[A-Za-z]", text):
        continue

    # Rule 3: Case-insensitive duplicate removal
    normalized = text.lower()

    if normalized in seen:
        continue

    seen.add(normalized)
    cleaned_lines.append(text)

with open(output_file, "w", encoding="utf-8") as f:
    for line in cleaned_lines:
        f.write(line + "\n")

print(f"Cleaned OCR saved to: {output_file}")
print(f"Original lines: {len(lines)}")
print(f"Cleaned lines: {len(cleaned_lines)}")