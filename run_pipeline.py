from download_reel import download_reel
from pipeline_utils import process_video
from pathlib import Path

url = input("Paste Reel URL: ")

download_reel(url)

reel_id = url.split("/reel/")[1].split("/")[0]

video_path = Path(f"downloads/{reel_id}.mp4")

process_video(video_path)