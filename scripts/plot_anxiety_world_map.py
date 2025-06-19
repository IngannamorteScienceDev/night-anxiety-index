import pandas as pd
import plotly.express as px
from pathlib import Path

# Пути
DATA_PATH = Path("data/processed/anxiety_prevalence_2019.csv")
OUTPUT_PATH = Path("outputs/plots/anxiety_map.png")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

def main():
    # Загрузка данных
    df = pd.read_csv(DATA_PATH)

    # Строим интерактивную хлороплет-карту
    fig = px.choropleth(
        df,
        locations="Country_Code",
        color="Anxiety_Prevalence_%",
        hover_name="Country",
        color_continuous_scale="OrRd",
        range_color=(df["Anxiety_Prevalence_%"].min(), df["Anxiety_Prevalence_%"].max()),
        title="Anxiety Prevalence by Country (2019)",
        labels={"Anxiety_Prevalence_%": "Prevalence (%)"}
    )

    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=False),
        title_x=0.5,
        margin={"r":0,"t":50,"l":0,"b":0}
    )

    # Показываем в браузере
    fig.show()

    # Сохраняем как PNG (kaleido)
    try:
        fig.write_image(str(OUTPUT_PATH), width=1200, height=600)
        print(f"✅ Saved static map to: {OUTPUT_PATH}")
    except Exception as e:
        print(f"⚠️ Could not save static image: {e}")
        print("Install kaleido via: pip install -U kaleido")

if __name__ == "__main__":
    main()
