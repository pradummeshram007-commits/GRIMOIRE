from pathlib import Path

metadata_folder = Path("metadata")

all_reels = []

for reel_folder in metadata_folder.iterdir():

    if reel_folder.is_dir():

        summary_file = reel_folder / "summary.txt"

        if summary_file.exists():

            with open(summary_file, "r", encoding="utf-8") as f:

                summary_text = f.read()

            topic = "Unknown"

            for line in summary_text.splitlines():

                if "topic" in line.lower():

                    topic = line.replace("**", "").replace("Topic:", "").strip()
                    break

            all_reels.append({
                "reel_id": reel_folder.name,
                "summary": summary_text,
                "topic": topic
            })

print(f"Loaded {len(all_reels)} reels\n")



#"""Store scores instead of printing immediately"""
query = input("Search: ").lower()

results = []

for reel in all_reels:

    summary = reel["summary"].lower()

    score = 0

    for word in query.split():

        score += summary.count(word)

    results.append({
        "reel_id": reel["reel_id"],
        "score": score,
        "summary": reel["summary"],
        "topic": reel["topic"]
    })


#Sort by score
results.sort(
    key=lambda x: x["score"],
    reverse=True
)

#Show only useful results
print("\nRESULTS\n")

for result in results:

    if result["score"] == 0:
        continue

    print(f"Topic: {result['topic']}")
    print(f"Reel ID: {result['reel_id']}")
    print(f"Score: {result['score']}")
    print("-" * 40)
    print(result["summary"][:300])