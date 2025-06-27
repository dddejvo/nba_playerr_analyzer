import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import pickle
import os

try:
    from xgboost import XGBRegressor
    xgb_installed = True
except ImportError:
    xgb_installed = False

def load_and_prepare_data(csv_path):
    df = pd.read_csv(csv_path)

    features = [
        "G", "MP", "FGA", "3PA", "FTA", "AST",
        "TRB", "STL", "BLK", "FG%", "3P%", "FT%"
    ]
    target = "PTS"

    df[features + [target]] = df[features + [target]].apply(pd.to_numeric, errors="coerce")
    df = df.dropna(subset=features + [target])

    df["FGA_per_MP"] = df["FGA"] / df["MP"]
    features.append("FGA_per_MP")

    df = df[(df["MP"] >= 100) & (df["G"] >= 10)]
    #print(f"Final dataset size: {len(df)} players")

    X = df[features]
    y = df[target]

    return X, y, df

def train_and_evaluate_model(model, model_name, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    rmse = root_mean_squared_error(y_test, preds)

    #print(f"\n {model_name}:")
    #print(f" MAE: {mae:.2f}")
    #print(f" RMSE: {rmse:.2f}")

    plot_predictions_vs_actual(y_test, preds, model_name)
    save_model(model, model_name)

    return {"model": model_name, "MAE": mae, "RMSE": rmse}

def plot_predictions_vs_actual(y_test, preds, model_name):
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, preds, alpha=0.7, label="Players")
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label="Perfect prediction (y = x)")
    plt.xlabel("Actual PTS")
    plt.ylabel("Predicted PTS")
    plt.title(f"{model_name}: Predicted vs Actual PTS")
    plt.legend()
    plt.tight_layout()

    os.makedirs("data", exist_ok=True)
    filename = f"data/{model_name.lower().replace(' ', '_')}_predicted_vs_actual.png"
    plt.savefig(filename)
    #print(f"Saved {model_name} plot to {filename}")
    plt.close()

def save_model(model, model_name):
    path = f"data/{model_name.lower().replace(' ', '_')}_model.pkl"
    os.makedirs("data", exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(model, f)
    #print(f" Saved {model_name} model to {path}")

def compare_models(X_train, X_test, y_train, y_test):
    models = [
        (RandomForestRegressor(random_state=42), "RandomForest"),
        (LinearRegression(), "LinearRegression")
    ]

    if xgb_installed:
        models.append((XGBRegressor(random_state=42), "XGBoost"))
    else:
        print("⚠ XGBoost not installed, skipping.")

    results = []
    for model, name in models:
        res = train_and_evaluate_model(model, name, X_train, y_train, X_test, y_test)
        results.append(res)

    summary_df = pd.DataFrame(results)
    summary_df.to_csv("data/model_comparison_summary.csv", index=False)
    #print(" Saved summary to data/model_comparison_summary.csv")
    return summary_df
