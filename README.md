# NBA Player Analyzer

This project provides tools for scraping, processing, analyzing, and visualizing NBA player statistics. It supports building and comparing machine learning models that predict player points based on season data.

---

##  Features
- **Scraper**: Downloads and cleans NBA player data from Basketball Reference for multiple seasons.
- **Pipeline**: Trains and compares multiple ML models (Random Forest, Linear Regression, XGBoost if installed), generates visualizations, and exports a PDF report.
- **Visualization**: Creates bar plots for top players in FG%, points per minute, and assists per game.
- **Report**: Combines generated plots into a single PDF report.

---

##  Project structure
```plaintext
nba_player_analyzer/
 ├── data/                  # Stores CSV data, models, plots, reports
 ├── scraper.py             # Script for scraping and cleaning NBA data
 ├── ml_model.py            # Module for training and evaluating ML models
 ├── viz.py                 # Visualization functions
 ├── generate_report.py      # Generates PDF report from plots
 ├── pipeline.py             # Main pipeline combining all components
 └── requirements.txt        # Required Python packages
```


  
---

##  Usage

###  Scrape data
Run the scraper to download and clean data for multiple seasons:
```bash
python scraper.py
``` 
Run the pipeline to train models, generate visualizations, and create a PDF report:
```bash
python pipeline.py
```
