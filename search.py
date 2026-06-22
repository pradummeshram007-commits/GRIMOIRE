from pathlib import Path

metadata_folder = Path("metadata")

all_reels = []

for reel_folder in metadata_folder.iterdir():

    if reel_folder.is_dir():

        summary_file = reel_folder / "summary.txt"

        if summary_file.exists():

            with open(summary_file, "r", encoding="utf-8") as f:

                summary_text = f.read()

            all_reels.append({
                "reel_id": reel_folder.name,
                "summary": summary_text
            })

print(f"Loaded {len(all_reels)} reels\n")

query = input("Search: ").lower()

print("\nRESULTS\n")

for reel in all_reels:

    summary = reel["summary"].lower()

    score = 0

    for word in query.split():

        score += summary.count(word)

    print(f"{reel['reel_id']} -> Score: {score}")