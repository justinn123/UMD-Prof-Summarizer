import planetterp
import json
import time
import csv

def fetch_all_professors():
    all_profs = []
    offset = 0
    limit = 100

    while True:
        batch = planetterp.professors(type_="professor", limit=limit, offset=offset)
        if not batch:
            break
        all_profs.extend(batch)
        print(f"Fetched {len(batch)} at offset {offset}")
        offset += limit
        time.sleep(0.2)  # Be nice to the server

    return all_profs

# Usage
all_professors = fetch_all_professors()
with open("professors.json", "w") as f:
    json.dump([p["name"] for p in all_professors], f, indent=2)

