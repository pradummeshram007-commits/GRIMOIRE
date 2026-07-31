from download_reel import download_reel
from pipeline_utils import process_video
from pathlib import Path
import json
from datetime import datetime

# Prompt user for the target Instagram Reel URL
url = input("Paste Reel URL: ")

# Attempt to download the video using yt-dlp wrapper
success = download_reel(url)

# Halt execution if the download fails to prevent cascading errors in downstream processing
if not success:
    print("Stopping pipeline.")
    exit()

# Extract the unique Reel ID from the URL string
# Example URL: https://www.instagram.com/reel/DYPFRgoTeC3/
# Splitting by "/reel/" gives "DYPFRgoTeC3/", and splitting by "/" extracts just "DYPFRgoTeC3"
reel_id = url.split("/reel/")[1].split("/")[0]

# Ensure the destination directory for this specific reel's metadata exists
metadata_path = Path(f"metadata/{reel_id}")
metadata_path.mkdir(parents=True, exist_ok=True)

# Construct foundational metadata to track the source and ingestion time
info = {
    "id": reel_id,
    "source": "instagram",
    "type": "reel",
    "url": url,
    "downloaded_at": datetime.now().isoformat()
}

# Persist the foundational metadata as a JSON file for future reference by the search indexer
with open(metadata_path / "info.json", "w", encoding="utf-8") as f:
    json.dump(info, f, indent=4)

# Define the path to the downloaded video file (saved by yt-dlp)
video_path = Path(f"downloads/{reel_id}.mp4")

# Trigger the main extraction and AI summarization pipeline on the downloaded video
process_video(video_path)