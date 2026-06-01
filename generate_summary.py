import subprocess
from pathlib import Path

# Transcript file
transcript_path = Path("metadata/reel1/transcript.txt")

# Read transcript
with open(transcript_path, "r", encoding="utf-8") as f:
    transcript = f.read()

prompt = f"""
You are an expert content understanding engine.

Your job is to analyze saved content and generate metadata that will help future search and organization.

Rules:
- Focus on the MAIN IDEA.
- Ignore filler speech and repetitive phrases.
- Extract practical value.
- Generate search-friendly keywords.
- Infer the most appropriate collection.
- Think like a knowledge management system.
- Important entities must always be extracted when present.

Return ONLY in this exact format:


Topic:
(Topic Rules:
- Prefer actual product names.
- Prefer actual course names.
- Prefer actual recipe names.
- Prefer actual technology names.
- Do not create generic titles.
)


Summary:

Key Takeaways:
- ...
- ...
- ...

Important Names:
(List all important entities mentioned or implied.

Include:
- Products
- Tools
- Companies
- Platforms
- Technologies
- Brands
- Courses
- Books
- AI models
- People

Never leave this section empty if notable entities exist and Return 3-10 entities whenever possible.)



Why Save:

(Describe the practical reason a human would save this content.
Focus on:
- future reference
- learning
- implementation
- problem solving
- inspiration
Avoid generic statements.)



Assigned Collection:


Search Keywords:
(Generate 8-15 highly searchable keywords and phrases.
Rules:
- Include product names.
- Include company names.
- Include tool names.
- Include technologies.
- Include common search phrases a user might type.
- Include beginner-friendly wording.
- Include advanced wording.
- Include alternative wording.

Avoid vague keywords like:
innovation
technology
tool
solution
platform

Keywords should maximize future search accuracy.)
- ...
- ...
- ...
- ...
- ...

Content:
{transcript}
"""

print("Generating summary...")

result = subprocess.run(
    ["ollama", "run", "qwen2.5:3b"],
    input=prompt,
    capture_output=True,
    text=True,
    encoding="utf-8"
)

import re

summary = result.stdout

# Remove ANSI escape sequences
summary = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', summary)

# Remove leftover ESC text if present
summary = re.sub(r'ESC\[[0-9;]*[A-Za-z]', '', summary)

# Save summary
summary_path = Path("metadata/reel1/summary.txt")

with open(summary_path, "w", encoding="utf-8") as f:
    f.write(summary)

print(f"Summary saved to: {summary_path}")