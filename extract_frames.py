import os
import subprocess

# Input video path
video_path = "downloads/reel1.mp4"

# Output folder for frames
output_folder = "frames/reel1"

# Create folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# FFmpeg command
command = [
    "ffmpeg",
    "-i", video_path,
    "-vf", "fps=1/2",
    f"{output_folder}/frame_%03d.jpg"
]

# Run command
subprocess.run(command)

print("Frames extracted successfully!")