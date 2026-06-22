import os
import subprocess
from pathlib import Path
import whisper
import easyocr
import re
import gc


def extract_frames(video_path, reel_id):

    frames_folder = Path(f"frames/{reel_id}")

    frames_folder.mkdir(parents=True, exist_ok=True)

    command = [
        "ffmpeg",
        "-i",
        str(video_path),
        "-vf",
        "fps=1/2",
        f"{frames_folder}/frame_%03d.jpg"
    ]

    subprocess.run(command)

    print(f"Frames extracted for {reel_id}")

    return frames_folder

def get_all_videos():
    downloads = Path("downloads")

    videos = []

    for file in downloads.iterdir():
        if file.suffix.lower() == ".mp4":
            videos.append(file)

    return videos


def get_reel_id(video_path):
    return video_path.stem


def create_folders(reel_id):
    frames_folder = Path(f"frames/{reel_id}")
    metadata_folder = Path(f"metadata/{reel_id}")

    frames_folder.mkdir(parents=True, exist_ok=True)
    metadata_folder.mkdir(parents=True, exist_ok=True)

    return frames_folder, metadata_folder



def transcribe_video(video_path, reel_id):

    print(f"Transcribing {reel_id}...")
    model = whisper.load_model("small")

    result = model.transcribe(  
    str(video_path),
    task="translate"
    
)

    transcript = result["text"]

    transcript_path = f"metadata/{reel_id}/transcript.txt"

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    print(f"Transcript saved for {reel_id}")

    del model

    import gc
    gc.collect()
    return transcript_path
    



def run_ocr(reel_id):

    reader = easyocr.Reader(['en'])
    frames_folder = f"frames/{reel_id}"
    metadata_folder = f"metadata/{reel_id}"

    output_file = os.path.join(metadata_folder, "ocr.txt")

    all_text = set()

    for file in sorted(os.listdir(frames_folder)):

        if file.endswith(".jpg"):

            image_path = os.path.join(frames_folder, file)

            print(f"OCR reading: {file}")

            result = reader.readtext(image_path, detail=0)

            for text in result:

                cleaned = text.strip()

                if cleaned:
                    all_text.add(cleaned)

    with open(output_file, "w", encoding="utf-8") as f:

        for text in sorted(all_text):
            f.write(text + "\n")

    print(f"OCR saved for {reel_id}")
    del reader

    import gc
    gc.collect()


def clean_ocr(reel_id):

    input_file = f"metadata/{reel_id}/ocr.txt"
    output_file = f"metadata/{reel_id}/cleaned_ocr.txt"

    seen = set()
    cleaned_lines = []

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:

        text = line.strip()

        if not text:
            continue

        # Rule 1
        if len(text) < 3:
            continue

        # Rule 2
        if not re.search(r"[A-Za-z]", text):
            continue

        normalized = text.lower()

        # Rule 3
        if normalized in seen:
            continue

        seen.add(normalized)
        cleaned_lines.append(text)

    with open(output_file, "w", encoding="utf-8") as f:

        for line in cleaned_lines:
            f.write(line + "\n")

    print(f"Clean OCR saved for {reel_id}")
    print(f"Original lines: {len(lines)}")
    print(f"Cleaned lines: {len(cleaned_lines)}")



def generate_summary(reel_id):

    import subprocess
    import re
    from pathlib import Path

    transcript_path = Path(f"metadata/{reel_id}/transcript.txt")
    cleaned_ocr_path = Path(f"metadata/{reel_id}/cleaned_ocr.txt")

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    with open(cleaned_ocr_path, "r", encoding="utf-8") as f:
        ocr_text = f.read()

    prompt = f"""
You are an expert content understanding engine.

Your job is to analyze noisy real-world content and generate metadata that will help future search and organization.

IMPORTANT:

The content comes from two sources:

1. Transcript (audio understanding)
2. OCR (text extracted from video frames)

Neither source is guaranteed to be accurate.
If OCR and Transcript conflict, prefer the interpretation that creates the most coherent and useful real-world meaning.

Rules:

- Use BOTH Transcript and OCR.
- Cross-check information between them.
- If Transcript is poor but OCR is meaningful, rely more on OCR.
- If OCR is poor but Transcript is meaningful, rely more on Transcript.
- If both contain useful information, combine them.
- If both contain errors, infer the most likely meaning.
- Never reject content simply because it contains OCR mistakes or transcription mistakes.
- Never output empty sections.
- Never output "None", "Not Applicable", or similar responses.
- Always attempt to identify the topic.
- Always generate useful search keywords.
- Even if confidence is low, provide the best possible interpretation.

Think like a human trying to understand an imperfect screenshot and imperfect audio recording.

Your goal is maximizing future searchability and retrieval accuracy.




Format Rules:
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
- Do not write None
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
(Assign the most relevant collection based on the content.
Examples:
- Productivity
- Health
- Finance
- Cooking
- Technology
- Education
- Lifestyle
- Design
- Fitness
- Travel
If content is highly specific, suggest a new collection name.)

Search Keywords:
Search Keywords are the MOST IMPORTANT section.
Assume future search will primarily rely on these keywords.
Generate keywords that users are actually likely to type into a search bar.
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

TRANSCRIPT:
{transcript}

OCR:
{ocr_text}
"""

    print(f"Generating summary for {reel_id}...")

    result = subprocess.run(
        ["ollama", "run", "qwen2.5:3b"],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    print("====== STDOUT ======")
    print(result.stdout)

    print("====== STDERR ======")
    print(result.stderr)


    summary = result.stdout

    summary = re.sub(
        r'\x1b\[[0-9;]*[A-Za-z]',
        '',
        summary
    )

    summary = re.sub(
        r'ESC\[[0-9;]*[A-Za-z]',
        '',
        summary
    )

    summary_path = Path(
        f"metadata/{reel_id}/summary.txt"
    )

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"Summary saved for {reel_id}")


def process_video(video_path):

    reel_id = get_reel_id(video_path)

    create_folders(reel_id)

    extract_frames(video_path, reel_id)
    transcribe_video(video_path, reel_id)
    run_ocr(reel_id)
    clean_ocr(reel_id)
    generate_summary(reel_id)

    print(f"Pipeline completed for {reel_id}")