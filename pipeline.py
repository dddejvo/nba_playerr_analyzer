import pandas as pd
from sklearn.model_selection import train_test_split
import os
import logging

from ml_model import load_and_prepare_data, compare_models
from viz import apply_min_playtime_filter, plot_extended
from generate_report import generate_pdf

# Nastavenie logovania
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("data/pipeline.log", mode="w", encoding="utf-8")
    ]
)

def check_data_exists(data_path):
    if not os.path.exists(data_path):
        logging.error(f"Data file '{data_path}' not found. Please run scraper.py first.")
        return False
    return True

def run_pipeline(data_path="data/nba_combined_totals_cleaned.csv", plot_dir="data/plots", report_path="data/nba_pipeline_report.pdf"):
    # Skontroluj dáta
    if not check_data_exists(data_path):
        return

    # Načítanie a príprava dát
    logging.info("Loading and preparing data...")
    X, y, df_full = load_and_prepare_data(data_path)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Tréning a porovnanie modelov
    logging.info("Training and evaluating models...")
    summary_df = compare_models(X_train, X_test, y_train, y_test)
    logging.info(f"\n{summary_df}")

    # Vizualizácie
    logging.info("Generating visualizations...")
    os.makedirs(plot_dir, exist_ok=True)
    df_filtered = apply_min_playtime_filter(df_full)
    plot_extended(df_filtered, save_path=plot_dir)

    # Report
    logging.info("Generating PDF report...")
    generate_pdf(plot_dir, report_path)

    logging.info(" Pipeline finished successfully.")

if __name__ == "__main__":
    run_pipeline()
