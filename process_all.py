
from pipeline_utils import transcribe_video
from pipeline_utils import run_ocr
from pipeline_utils import *

videos = get_all_videos()

print(f"Found {len(videos)} videos")

for video in videos:

    reel_id = get_reel_id(video)

    print("\n-------------------")
    print(f"Processing: {reel_id}")

    frames_folder, metadata_folder = create_folders(reel_id)

    extract_frames(video, reel_id)
    transcribe_video(video, reel_id)
    run_ocr(reel_id)
    clean_ocr(reel_id)
    generate_summary(reel_id)