import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ANXIETY_PATH = BASE_DIR / "data/processed/anxiety_prevalence_2019.csv"
LIGHT_PATH = BASE_DIR / "data/processed/nightlight_2019.csv"
OUTPUT_PATH = BASE_DIR / "data/processed/df_model.csv"

def main():
    print("📥 Loading datasets...")
    df_anxiety = pd.read_csv(ANXIETY_PATH)
    df_light = pd.read_csv(LIGHT_PATH)

    print("🔗 Merging on Country_Code...")
    df_merged = pd.merge(df_anxiety, df_light, on="Country_Code", how="inner")

    print(f"✅ Merged dataset: {df_merged.shape[0]} rows")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_merged.to_csv(OUTPUT_PATH, index=False)
    print(f"💾 Saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
