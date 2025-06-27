import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_nba_totals(season_year: int) -> pd.DataFrame:
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
    df["Season"] = season_year

    return df

def clean_nba_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.iloc[:-1]

    team_col = "Tm"
    if "Tm" not in df.columns and "Team" in df.columns:
        team_col = "Team"

    multi_team_players = df[df[team_col].str.contains("TM")]["Player"].unique()

    df_clean = df[
        (df[team_col].str.contains("TM")) | 
        (~df["Player"].isin(multi_team_players))
    ].reset_index(drop=True)

    return df_clean

def scrape_multiple_seasons(start_year: int, end_year: int, save_path: str = "data"):
    os.makedirs(save_path, exist_ok=True)
    dfs = []

    for year in range(start_year, end_year + 1):
        df_raw = scrape_nba_totals(year)
        if df_raw is not None:
            df_clean = clean_nba_data(df_raw)
            file_path = os.path.join(save_path, f"nba_{year}_totals_cleaned.csv")
            df_clean.to_csv(file_path, index=False, encoding="utf-8")
            #print(f" Saved cleaned data to {file_path}")
            dfs.append(df_clean)

    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_file = os.path.join(save_path, "nba_combined_totals_cleaned.csv")
        combined_df.to_csv(combined_file, index=False, encoding="utf-8")
        #print(f" Saved combined data to {combined_file}")
    else:
        print("⚠ No data scraped for the given range.")

if __name__ == "__main__":
    path = "data"
    scrape_multiple_seasons(2020, 2025, path)
