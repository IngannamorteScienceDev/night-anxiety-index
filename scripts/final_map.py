import pandas as pd
import plotly.express as px
from pathlib import Path
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

# Define base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Define paths to input data, trained model, and output plot
DATA_PATH = BASE_DIR / "data/processed/df_model.csv"
MODEL_PATH = BASE_DIR / "models/randomforest_model.joblib"  # You may change to another model
PLOT_PATH = BASE_DIR / "outputs/plots/final_anxiety_map.html"

def main():
    # Step 1: Load merged dataset
    df = pd.read_csv(DATA_PATH)

    # Step 2: Prepare feature for prediction (log-transform and scale light intensity)
    X = df[["Light_Intensity"]].copy()
    X["Light_Intensity"] = np.log1p(X["Light_Intensity"])
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Step 3: Load model and generate predictions
    model = joblib.load(MODEL_PATH)
    df["Predicted_Anxiety"] = model.predict(X_scaled)
    df["Residual"] = df["Anxiety_Prevalence_%"] - df["Predicted_Anxiety"]

    # Step 4: Generate interactive choropleth map
    fig = px.choropleth(
        df,
        locations="Country_Code",
        color="Anxiety_Prevalence_%",
        hover_name="Country" if "Country" in df.columns else None,
        color_continuous_scale="YlOrRd",
        title="Real Anxiety Prevalence by Country (2019)",
        labels={"Anxiety_Prevalence_%": "Anxiety %"},
        projection="natural earth"
    )

    # Step 5: Update layout and save to HTML
    fig.update_layout(title_x=0.5)
    fig.write_html(PLOT_PATH)

    print(f"Saved interactive map to: {PLOT_PATH}")

if __name__ == "__main__":
    main()
