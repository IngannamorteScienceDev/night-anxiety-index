import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data/processed/df_model.csv"
MODEL_DIR = BASE_DIR / "models"
PLOT_DIR = BASE_DIR / "outputs/plots"

MODELS = {
    "LinearRegression": MODEL_DIR / "linearregression_model.joblib",
    "RandomForest": MODEL_DIR / "randomforest_model.joblib",
    "XGBoost": MODEL_DIR / "xgboost_model.joblib"
}

def main():
    df = pd.read_csv(DATA_PATH)

    X = df[["Light_Intensity"]].copy()
    y = df["Anxiety_Prevalence_%"]

    X["Light_Intensity"] = np.log1p(X["Light_Intensity"])
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    for name, path in MODELS.items():
        print(f"📦 Loading model: {name}")
        model = joblib.load(path)
        preds = model.predict(X_scaled)

        # Scatter: Actual vs Predicted
        plt.figure(figsize=(6, 5))
        sns.scatterplot(x=y, y=preds, alpha=0.7)
        plt.xlabel("Actual Anxiety Rate (%)")
        plt.ylabel("Predicted")
        plt.title(f"{name} – Actual vs Predicted")
        plt.plot([y.min(), y.max()], [y.min(), y.max()], color="red", linestyle="--")
        plt.tight_layout()
        plt.savefig(PLOT_DIR / f"{name.lower()}_pred_vs_actual.png")
        plt.clf()

        # Residuals
        residuals = y - preds
        sns.histplot(residuals, kde=True)
        plt.title(f"{name} – Residuals Distribution")
        plt.xlabel("Residual (Actual - Predicted)")
        plt.tight_layout()
        plt.savefig(PLOT_DIR / f"{name.lower()}_residuals.png")
        plt.clf()

    print("✅ Visualization complete. Plots saved.")

if __name__ == "__main__":
    main()
