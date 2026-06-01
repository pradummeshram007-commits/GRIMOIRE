import whisper
import os

print("Loading model...")
model = whisper.load_model("base")

print("Transcribing...")
result = model.transcribe("downloads/reel1.mp4")

transcript = result["text"]

# Create metadata folder if needed
os.makedirs("metadata/reel1", exist_ok=True)

# Save transcript
with open("metadata/reel1/transcript.txt", "w", encoding="utf-8") as f:
    f.write(transcript)

print("\nTranscript saved to metadata/reel1/transcript.txt")