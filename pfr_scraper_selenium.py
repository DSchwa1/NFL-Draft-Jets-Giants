from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Setup Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

all_picks = []

for year in range(1994, 2025):
    url = f"https://www.pro-football-reference.com/years/{year}/draft.htm"
    driver.get(url)
    time.sleep(3)  # wait for page to load
    
    soup = BeautifulSoup(driver.page_source, "lxml")
    
    # Print table IDs for debugging
    tables = soup.find_all("table")
    table_ids = [t.get("id") for t in tables]
    print(f"{year}: found tables: {table_ids}")
    
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
            # Only grab round 1
            round_num = cols[0].get_text(strip=True)
            if round_num != "1":
                continue
                
            pick_data = {
                "year": year,
                "round": round_num,
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
    
    print(f"{year}: {year_count} round 1 picks saved")
    time.sleep(2)

driver.quit()

df = pd.DataFrame(all_picks)
df.to_csv("pfr_round1_draft_data.csv", index=False)
print(f"\nDone. {len(df)} total picks saved to pfr_round1_draft_data.csv")
