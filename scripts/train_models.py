import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from joblib import dump
from math import sqrt

# Define file paths
DATA_PATH = "data/processed/df_model.csv"
MODEL_DIR = "models"

def evaluate_model(model, X_test, y_test, name):
    """
    Evaluate the performance of a trained model on test data.
    Computes MAE, RMSE, and R^2 score.
    """
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = sqrt(mean_squared_error(y_test, preds))  # Manually compute RMSE
    r2 = r2_score(y_test, preds)

    # Print evaluation metrics
    print(f"\n{name} Evaluation:")
    print(f"   MAE:  {mae:.4f}")
    print(f"   RMSE: {rmse:.4f}")
    print(f"   R²:   {r2:.4f}")

    return {
        "Model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }

def main():
    # Load the processed dataset
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)

    # Extract feature(s) and target variable
    X = df[["Light_Intensity"]]
    y = df["Anxiety_Prevalence_%"]

    # Split the dataset into training and test sets (80/20 split)
    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Normalize the features using StandardScaler
    print("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Define the models to train
    print("Training models...")
    models = [
        ("LinearRegression", LinearRegression()),
        ("RandomForest", RandomForestRegressor(random_state=42)),
        ("XGBoost", XGBRegressor(random_state=42))
    ]

    # Train and evaluate each model
    results = []
    for name, model in models:
        model.fit(X_train_scaled, y_train)
        results.append(evaluate_model(model, X_test_scaled, y_test, name))

        # Save the trained model to disk
        model_path = os.path.join(MODEL_DIR, f"{name.lower()}_model.joblib")
        dump(model, model_path)
        print(f"Saved {name} model to {model_path}")

    # Save all evaluation results to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv("outputs/reports/model_results.csv", index=False)
    print("Model evaluation results saved to outputs/reports/model_results.csv")

if __name__ == "__main__":
    main()
