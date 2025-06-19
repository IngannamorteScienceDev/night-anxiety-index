import pandas as pd
from pathlib import Path

# Define the absolute path to the project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Define paths to input (raw) and output (processed) data files
RAW_PATH = BASE_DIR / "data/raw/VIIRS-nighttime-lights-2013m1to2024m5-level0.csv"
PROCESSED_PATH = BASE_DIR / "data/processed/nightlight_2019.csv"

def main():
    # Step 1: Load the raw CSV data
    print("Loading nightlight CSV...")
    df = pd.read_csv(RAW_PATH)

    # Step 2: Filter records for the year 2019
    print("Filtering for year 2019...")
    df_2019 = df[df["year"] == 2019]

    # Step 3: Group by ISO country code and calculate average nightlight sum
    print("Grouping by country and averaging nlsum...")
    df_grouped = df_2019.groupby("iso", as_index=False)["nlsum"].mean()

    # Rename columns for clarity
    df_grouped.columns = ["Country_Code", "Light_Intensity"]

    # Step 4: Save the processed data to a new CSV file
    print("Saving processed file to disk...")
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_grouped.to_csv(PROCESSED_PATH, index=False)

    print(f"Finished. Output saved to: {PROCESSED_PATH}")

if __name__ == "__main__":
    main()
