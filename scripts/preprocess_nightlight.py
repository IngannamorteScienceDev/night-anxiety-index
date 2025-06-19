import pandas as pd
import requests
from pathlib import Path
from io import StringIO
from time import sleep

RAW_PATH = Path("data/raw/")
PROCESSED_PATH = Path("data/processed/nightlight_2019.csv")
ANXIETY_PATH = Path("data/processed/anxiety_prevalence_2019.csv")
S3_BASE_URL = "https://nightlightdata.s3.amazonaws.com/monthly-csvs/adm0"

def download_csv_from_s3(iso_code):
    url = f"{S3_BASE_URL}/{iso_code}.csv"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return pd.read_csv(StringIO(response.text))
        else:
            print(f"⚠️ No data for {iso_code} (HTTP {response.status_code})")
            return None
    except Exception as e:
        print(f"❌ Failed to download {iso_code}: {e}")
        return None

def main():
    # Загружаем список стран
    anxiety_df = pd.read_csv(ANXIETY_PATH)
    iso_list = anxiety_df["Country_Code"].dropna().unique()

    records = []

    for iso in iso_list:
        print(f"⬇ Downloading: {iso}")
        df = download_csv_from_s3(iso)
        sleep(0.5)  # чтобы не перегружать сервер

        if df is None or df.empty:
            continue

        if 'year' not in df.columns or 'mean' not in df.columns:
            print(f"⚠️ Missing expected columns in {iso}")
            continue

        df_2019 = df[df['year'] == 2019]
        if df_2019.empty:
            print(f"⚠️ No 2019 data for {iso}")
            continue

        mean_light = df_2019['mean'].mean()
        records.append({"Country_Code": iso, "Light_Intensity": mean_light})

    result_df = pd.DataFrame(records)
    print(f"✅ Collected data for {len(result_df)} countries")

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(PROCESSED_PATH, index=False)
    print(f"💾 Saved to {PROCESSED_PATH}")

if __name__ == "__main__":
    main()
