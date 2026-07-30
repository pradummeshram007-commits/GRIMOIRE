from download_reel import download_reel
from pipeline_utils import process_video
from pathlib import Path
import json
from datetime import datetime

url = input("Paste Reel URL: ")

success = download_reel(url)

if not success:
    print("Stopping pipeline.")
    exit()

reel_id = url.split("/reel/")[1].split("/")[0]


metadata_path = Path(f"metadata/{reel_id}")
metadata_path.mkdir(parents=True, exist_ok=True)

info = {
    "id": reel_id,
    "source": "instagram",
    "type": "reel",
    "url": url,
    "downloaded_at": datetime.now().isoformat()
}

with open(metadata_path / "info.json", "w", encoding="utf-8") as f:
    json.dump(info, f, indent=4)

video_path = Path(f"downloads/{reel_id}.mp4")

process_video(video_path)