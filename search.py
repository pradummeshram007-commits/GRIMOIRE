from pathlib import Path
import webbrowser
import json

metadata_folder = Path("metadata")

def extract_section(text, section_name):

    lines = text.splitlines()

    capture = False
    collected = []

    for line in lines:

        if section_name.lower() in line.lower():
            capture = True
            continue

        if capture and line.startswith("**") and section_name.lower() not in line.lower():
            break

        if capture:
            collected.append(line)

    return " ".join(collected).strip()

all_reels = []

for reel_folder in metadata_folder.iterdir():

    if reel_folder.is_dir():

        summary_file = reel_folder / "summary.txt"
        info_file = reel_folder / "info.json"

        if summary_file.exists():

            with open(summary_file, "r", encoding="utf-8") as f:

                summary_text = f.read()

            topic = "Unknown"

            for line in summary_text.splitlines():

                if "topic" in line.lower():

                    topic = line.replace("**", "").replace("Topic:", "").strip()
                    break





            summary_section = extract_section(
                summary_text,
                "Summary"
            )

            why_save = extract_section(
                summary_text,
                "Why Save"
            )

            search_keywords = extract_section(
                summary_text,
            "Search Keywords"
            )

            url = ""

            if info_file.exists():
                with open(info_file, "r", encoding="utf-8") as f:
                    info = json.load(f)

                url = info.get("url", "")


            keywords = ""
            for line in summary_text.splitlines():

                if "Search Keywords" in line:
                    keywords = summary_text[
                        summary_text.find(line):
                    ]
                    break
                

            all_reels.append({ 
                "reel_id": reel_folder.name,
                "url": url,
                "summary": summary_text,
                "topic": topic,
                "summary_section": summary_section,
                "why_save": why_save,
                "search_keywords": search_keywords,
                "keywords": keywords   
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

        score += reel["topic"].lower().count(word) * 10

        score += reel["keywords"].lower().count(word) * 5
    
    
    
    
    
    results.append({
    
    "reel_id": reel["reel_id"],
    "url": reel["url"],
    "summary": reel["summary"],
    "topic": reel["topic"],
    "summary_section": reel["summary_section"],
    "why_save": reel["why_save"],
    "search_keywords": reel["search_keywords"],
    "keywords": reel["keywords"],
    "score": score
    })


#Sort by score
results.sort(
    key=lambda x: x["score"],
    reverse=True
)

#Show only useful results
'''print("\nRESULTS\n")

rank = 1
for result in results:
    
    if result["score"] == 0:
        continue
    
    print("=" * 50)
    print(f"{rank}.")
    print()
    
    print(f"Topic: {result['topic']}")
    print(f"Reel ID: {result['reel_id']}")
    print(f"Score: {result['score']}")

    print("\nSummary:")
    print(result["summary_section"])

    print("\nWhy Save:")
    print(result["why_save"])

    print("\n" + "=" * 50)
    
    rank += 1'''



'''print("\nRESULTS\n")

displayed_results = []

rank = 1

for result in results:

    if result["score"] == 0:
        continue

    displayed_results.append(result)

    print("=" * 50)
    print(f"{rank}.")
    print()

    print(f"Topic: {result['topic']}")
    print(f"Reel ID: {result['reel_id']}")
    print(f"Score: {result['score']}")

    print("\nSummary:")
    print(result["summary_section"])

    print("\nWhy Save:")
    print(result["why_save"])

    print("\n" + "=" * 50)

    rank += 1'''


print("\nRESULTS\n")

displayed_results = []

rank = 1

for result in results:

    if result["score"] == 0:
        continue

    displayed_results.append(result)

    print("=" * 50)
    print(f"{rank}. {result['topic']}")
    print()

    print(f"Topic: {result['topic']}")
    print(f"Reel ID: {result['reel_id']}")
    print(f"Score: {result['score']}")

    print("\nSummary:")
    print(result["summary_section"])

    print("\nWhy Save:")
    print(result["why_save"])

    print("\n" + "=" * 50)

    rank += 1
    


if displayed_results:

    choice = input(
        f"\nOpen a reel? (1-{len(displayed_results)} / n): "
    ).strip().lower()

    if choice != "n":

        if choice.isdigit():

            choice = int(choice)

            if 1 <= choice <= len(displayed_results):

                selected = displayed_results[choice - 1]

                print("Opening reel...")

                webbrowser.open(selected["url"])

            else:
                print("Invalid choice.")

        else:
            print("Invalid choice.")


webbrowser.open(selected["url"])