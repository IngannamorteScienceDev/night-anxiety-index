import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / "data/raw/VIIRS-nighttime-lights-2013m1to2024m5-level0.csv"
PROCESSED_PATH = BASE_DIR / "data/processed/nightlight_2019.csv"

def main():
    print("📥 Loading CSV...")
    df = pd.read_csv(RAW_PATH)

    print("🔍 Filtering for year 2019...")
    df_2019 = df[df["year"] == 2019]

    print("📊 Grouping by country and averaging light...")
    df_grouped = df_2019.groupby("iso_alpha3", as_index=False)["mean"].mean()
    df_grouped.columns = ["Country_Code", "Light_Intensity"]

    print("💾 Saving to processed CSV...")
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_grouped.to_csv(PROCESSED_PATH, index=False)
    print(f"✅ Done! Saved to: {PROCESSED_PATH}")

if __name__ == "__main__":
    main()
