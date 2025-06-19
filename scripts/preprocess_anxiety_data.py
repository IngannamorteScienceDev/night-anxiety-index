import pandas as pd
from pathlib import Path

# Пути к файлам
RAW_PATH = Path("data/raw/anxiety-disorders-prevalence.csv")
PROCESSED_PATH = Path("data/processed/anxiety_prevalence_2019.csv")

def main():
    # Загрузка данных
    try:
        df = pd.read_csv(RAW_PATH)
    except FileNotFoundError:
        print(f"❌ File not found: {RAW_PATH}")
        return

    # Выводим названия колонок для отладки
    print("📊 Available columns:", df.columns.tolist())

    # Фильтрация по году
    df_2019 = df[df["Year"] == 2019]
    print(f"✅ Filtered to {len(df_2019)} rows for 2019")

    # Переименование и отбор нужных колонок
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
        print("❌ Column not found:", e)
        return

    # Создание директории и сохранение
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(PROCESSED_PATH, index=False)
    print(f"✅ Processed data saved to: {PROCESSED_PATH}")

if __name__ == "__main__":
    main()
