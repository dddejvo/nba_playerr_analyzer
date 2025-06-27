# This script visualizes NBA player statistics from a CSV file.

import pandas as pd
import matplotlib.pyplot as plt
import os

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    return df

def plot_bar(df, column, title, xlabel, top_n=10, horizontal=True, save_path="data"):
    df[column] = pd.to_numeric(df[column], errors="coerce")
    top_df = df.sort_values(by=column, ascending=False).head(top_n)

    plt.figure(figsize=(10, 6))
    if horizontal:
        plt.barh(top_df["Player"], top_df[column])
        plt.xlabel(xlabel)
    else:
        plt.bar(top_df["Player"], top_df[column])
        plt.ylabel(xlabel)
        plt.xticks(rotation=30, ha='right')

    plt.title(title)
    plt.tight_layout()

    # Uloženie
    os.makedirs(save_path, exist_ok=True)
    filename = f"{title.replace(' ', '_').lower()}.png"
    filepath = os.path.join(save_path, filename)
    plt.savefig(filepath)
    print(f"✅ Saved graph to {filepath}")

    plt.show()

def main():
    csv_path = "data/nba_2025_totals_cleaned.csv"
    df = load_data(csv_path)

    plot_bar(df, "PTS", "Top 10 Scorers", "Total Points")
    plot_bar(df, "3P", "Top 10 3-Point Shooters", "3P Made")
    plot_bar(df, "AST", "Top 10 Assist Leaders", "Total Assists")
    plot_bar(df, "MP", "Top 10 Minutes Played", "Total Minutes")

if __name__ == "__main__":
    main()
