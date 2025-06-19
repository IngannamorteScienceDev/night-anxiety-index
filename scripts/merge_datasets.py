import pandas as pd
from pathlib import Path

# Define the base directory relative to the current script
BASE_DIR = Path(__file__).resolve().parent.parent

# Define paths to input datasets and output location
ANXIETY_PATH = BASE_DIR / "data/processed/anxiety_prevalence_2019.csv"
LIGHT_PATH = BASE_DIR / "data/processed/nightlight_2019.csv"
OUTPUT_PATH = BASE_DIR / "data/processed/df_model.csv"

def main():
    # Step 1: Load both preprocessed datasets
    print("Loading datasets...")
    df_anxiety = pd.read_csv(ANXIETY_PATH)
    df_light = pd.read_csv(LIGHT_PATH)

    # Step 2: Merge the datasets on the shared 'Country_Code' column
    print("Merging datasets on 'Country_Code'...")
    df_merged = pd.merge(df_anxiety, df_light, on="Country_Code", how="inner")

    # Step 3: Output merged dataset size
    print(f"Merged dataset contains {df_merged.shape[0]} rows.")

    # Step 4: Save the merged dataset to the processed folder
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_merged.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved merged dataset to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
