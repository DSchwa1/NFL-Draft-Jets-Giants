import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

# Exploratory scraper for Pro Football Reference draft data (1994-2024).
# The final analysis pipeline used nflverse instead — see combine.csv and the
# nflverse import instructions in the README.

all_picks = []

for year in range(1994, 2025):
    url = f"https://www.pro-football-reference.com/years/{year}/draft.htm"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")

        tables = soup.find_all("table")
        table = None
        for t in tables:
            if t.get("id"):
                table = t
                break

        if not table:
            print(f"{year}: no table found, skipping")
            continue

        rows = table.find("tbody").find_all("tr")
        year_count = 0
        
        for row in rows:
            if row.get("class") and "thead" in row.get("class"):
                continue
            cols = row.find_all(["td", "th"])
            if len(cols) < 8:
                continue
            try:
                pick_data = {
                    "year": year,
                    "round": cols[0].get_text(strip=True),
                    "pick": cols[1].get_text(strip=True),
                    "team": cols[2].get_text(strip=True),
                    "player": cols[3].get_text(strip=True),
                    "position": cols[4].get_text(strip=True),
                    "age": cols[5].get_text(strip=True),
                    "college": cols[6].get_text(strip=True),
                    "games": cols[7].get_text(strip=True),
                    "approximate_value": cols[11].get_text(strip=True) if len(cols) > 11 else ""
                }
                all_picks.append(pick_data)
                year_count += 1
            except Exception as e:
                continue
        
        print(f"{year}: {year_count} picks saved")
        
    except Exception as e:
        print(f"{year}: error — {e}")
    
    time.sleep(4)

df = pd.DataFrame(all_picks)
df.to_csv("pfr_draft_data.csv", index=False)
print(f"\nDone. {len(df)} total picks saved to pfr_draft_data.csv")