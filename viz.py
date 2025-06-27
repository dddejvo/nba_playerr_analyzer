import pandas as pd
import matplotlib.pyplot as plt
import os

def apply_min_playtime_filter(df, min_minutes=100, min_games=10):
    df["MP"] = pd.to_numeric(df["MP"], errors="coerce")
    df["G"] = pd.to_numeric(df["G"], errors="coerce")
    filtered_df = df[(df["MP"] >= min_minutes) & (df["G"] >= min_games)]
    #print(f" Filtered down to {len(filtered_df)} players with MP >= {min_minutes} and G >= {min_games}")
    return filtered_df

def plot_bar(df, players, values, title, xlabel, save_path="data"):
    plt.figure(figsize=(10, 6))
    plt.barh(players, values)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.tight_layout()

    os.makedirs(save_path, exist_ok=True)
    filename = f"{title.replace(' ', '_').lower()}.png"
    filepath = os.path.join(save_path, filename)
    plt.savefig(filepath)
    #print(f" Saved graph to {filepath}")
    plt.close()

def plot_extended(df, save_path="data"):
    for col in ["PTS", "G", "MP", "FG%", "AST"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # FG%
    df_fg = df[df["FG%"].notnull()]
    top_fg = df_fg.sort_values("FG%", ascending=False).head(10)
    plot_bar(top_fg, top_fg["Player"], top_fg["FG%"], "Top 10 FG% Shooters", "FG%", save_path)

    # Points per minute
    df["PTS_per_MP"] = df["PTS"] / df["MP"]
    top_pts_mp = df.sort_values("PTS_per_MP", ascending=False).head(10)
    plot_bar(top_pts_mp, top_pts_mp["Player"], top_pts_mp["PTS_per_MP"], "Top 10 PTS per Minute", "Points per Minute", save_path)

    # Assists per game
    df["AST_per_G"] = df["AST"] / df["G"]
    top_ast_g = df.sort_values("AST_per_G", ascending=False).head(10)
    plot_bar(top_ast_g, top_ast_g["Player"], top_ast_g["AST_per_G"], "Top 10 AST per Game", "Assists per Game", save_path)
