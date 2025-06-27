import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_nba_totals(season_year: int, save_path: str = "data"):
    url = f"https://www.basketball-reference.com/leagues/NBA_{season_year}_totals.html"
    print(f"Scraping data from: {url}")

    response = requests.get(url)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        print(f"Error: Unable to fetch data (status code {response.status_code})")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "totals_stats"})
    if table is None:
        print("Error: Could not find totals_stats table on the page")
        return None

    headers = [th.get_text(strip=True) for th in table.thead.find_all("th")]
    rows = []
    for row in table.tbody.find_all("tr"):
        if row.get("class") == ["thead"]:
            continue
        cells = [cell.get_text(strip=True) for cell in row.find_all(["th", "td"])]
        rows.append(cells)

    df = pd.DataFrame(rows, columns=headers)
    df = df[df["Rk"] != "Rk"].reset_index(drop=True)

    os.makedirs(save_path, exist_ok=True)
    full_csv = os.path.join(save_path, f"nba_{season_year}_totals_full.csv")
    df.to_csv(full_csv, index=False, encoding="utf-8")
    print(f"Full data saved to {full_csv}")
    
    return df

def clean_nba_data(df: pd.DataFrame, save_path: str, season_year: int):
    print("Cleaning data...")
    df = df.iloc[:-1]

    team_col = "Tm"
    if "Tm" not in df.columns and "Team" in df.columns:
        team_col = "Team"

    # Multi-team riadky sú tie, kde team_col obsahuje 'TM'
    multi_team_players = df[df[team_col].str.contains("TM")]["Player"].unique()

    df_clean = df[
        (df[team_col].str.contains("TM")) | 
        (~df["Player"].isin(multi_team_players))
    ].reset_index(drop=True)

    clean_csv = os.path.join(save_path, f"nba_{season_year}_totals_cleaned.csv")
    df_clean.to_csv(clean_csv, index=False)
    print(f"Cleaned data saved to {clean_csv}")
    


    

if __name__ == "__main__":
    season = 2025
    path = "data"
    
    df_scraped = scrape_nba_totals(season, path)
    if df_scraped is not None:
        clean_nba_data(df_scraped, path, season)

        
