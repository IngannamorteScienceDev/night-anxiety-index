import pandas as pd
from pathlib import Path

# Пути
RAW_PATH = Path("data/raw/anxiety-disorders-prevalence.csv")
PROCESSED_PATH = Path("data/processed/anxiety_prevalence_2019.csv")


def main():
    # Загрузка данных
    df = pd.read_csv(RAW_PATH)

    # Фильтрация по последнему году
    df_2019 = df[df["Year"] == 2019]

    # Переименование и выбор нужных колонок
    df_clean = df_2019[[
        "Entity", "Code", "Year", "Anxiety disorders (share of population)"
    ]].rename(columns={
        "Entity": "Country",
        "Code": "Country_Code",
        "Anxiety disorders (share of population)": "Anxiety_Prevalence_%"
    })

    # Сохранение
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(PROCESSED_PATH, index=False)
    print(f"Saved to: {PROCESSED_PATH}")


if __name__ == "__main__":
    main()
