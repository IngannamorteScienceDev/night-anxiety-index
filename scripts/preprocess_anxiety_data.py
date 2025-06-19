import pandas as pd
from pathlib import Path

# Define paths to the raw input and processed output CSV files
RAW_PATH = Path("data/raw/anxiety-disorders-prevalence.csv")
PROCESSED_PATH = Path("data/processed/anxiety_prevalence_2019.csv")

def main():
    # Step 1: Load raw CSV file
    try:
        df = pd.read_csv(RAW_PATH)
    except FileNotFoundError:
        print(f"[Error] File not found: {RAW_PATH}")
        return

    # Step 2: Print available columns for debugging
    print("Available columns in dataset:")
    print(df.columns.tolist())

    # Step 3: Filter data for the year 2019
    df_2019 = df[df["Year"] == 2019]
    print(f"Filtered to {len(df_2019)} rows for year 2019.")

    # Step 4: Select and rename required columns
    try:
        df_clean = df_2019[[
            "Entity",
            "Code",
            "Year",
            "Anxiety disorders (share of population) - Sex: Both - Age: Age-standardized"
        ]].rename(columns={
            "Entity": "Country",
            "Code": "Country_Code",
            "Anxiety disorders (share of population) - Sex: Both - Age: Age-standardized": "Anxiety_Prevalence_%"
        })
    except KeyError as e:
        print("[Error] Column not found:", e)
        return

    # Step 5: Save the cleaned DataFrame to CSV
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(PROCESSED_PATH, index=False)
    print(f"Processed data saved to: {PROCESSED_PATH}")

if __name__ == "__main__":
    main()
