import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path
from sklearn.preprocessing import StandardScaler

# Define base directory and important file paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data/processed/df_model.csv"
MODEL_DIR = BASE_DIR / "models"
PLOT_DIR = BASE_DIR / "outputs/plots"

# Dictionary mapping model names to their saved file paths
MODELS = {
    "LinearRegression": MODEL_DIR / "linearregression_model.joblib",
    "RandomForest": MODEL_DIR / "randomforest_model.joblib",
    "XGBoost": MODEL_DIR / "xgboost_model.joblib"
}

def main():
    # Load preprocessed dataset
    df = pd.read_csv(DATA_PATH)

    # Extract features and target
    X = df[["Light_Intensity"]].copy()
    y = df["Anxiety_Prevalence_%"]

    # Apply log transformation to Light_Intensity to reduce skewness
    X["Light_Intensity"] = np.log1p(X["Light_Intensity"])

    # Standardize features to zero mean and unit variance
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Loop through all saved models
    for name, path in MODELS.items():
        print(f"Loading model: {name}")

        # Load trained model from disk
        model = joblib.load(path)

        # Predict anxiety prevalence using the model
        preds = model.predict(X_scaled)

        # === 1. Scatter plot: Actual vs Predicted ===
        plt.figure(figsize=(6, 5))
        sns.scatterplot(x=y, y=preds, alpha=0.7)
        plt.xlabel("Actual Anxiety Rate (%)")
        plt.ylabel("Predicted Anxiety Rate (%)")
        plt.title(f"{name} – Actual vs Predicted")
        plt.plot([y.min(), y.max()], [y.min(), y.max()], color="red", linestyle="--")  # Reference line
        plt.tight_layout()
        plt.savefig(PLOT_DIR / f"{name.lower()}_pred_vs_actual.png")
        plt.clf()  # Clear figure for next plot

        # === 2. Histogram: Residuals distribution ===
        residuals = y - preds
        sns.histplot(residuals, kde=True)
        plt.title(f"{name} – Residuals Distribution")
        plt.xlabel("Residual (Actual - Predicted)")
        plt.tight_layout()
        plt.savefig(PLOT_DIR / f"{name.lower()}_residuals.png")
        plt.clf()  # Clear figure for next plot

    print("Visualization complete. Plots saved successfully.")

if __name__ == "__main__":
    main()
