from pathlib import Path

metadata_folder = Path("metadata")

for reel_folder in metadata_folder.iterdir():

    if reel_folder.is_dir():

        summary_file = reel_folder / "summary.txt"

        if summary_file.exists():

            print(reel_folder.name)