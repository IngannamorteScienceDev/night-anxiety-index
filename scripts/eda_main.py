import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data/processed/df_model.csv"
PLOT_DIR = BASE_DIR / "outputs/plots"
PLOT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(DATA_PATH)

    print("📈 Descriptive statistics:")
    print(df.describe())

    print("📊 Pearson correlation:")
    print(df.corr(numeric_only=True))

    # ✅ Используем правильное имя колонки
    sns.histplot(df["Anxiety_Prevalence_%"], kde=True)
    plt.title("Distribution of Anxiety Prevalence (%)")
    plt.savefig(PLOT_DIR / "hist_anxiety.png")
    plt.clf()

    sns.histplot(df["Light_Intensity"], kde=True)
    plt.title("Distribution of Light Intensity")
    plt.xscale("log")
    plt.savefig(PLOT_DIR / "hist_light.png")
    plt.clf()

    sns.scatterplot(x="Light_Intensity", y="Anxiety_Prevalence_%", data=df)
    plt.xscale("log")
    plt.title("Anxiety Prevalence vs Light Intensity")
    plt.savefig(PLOT_DIR / "scatter_light_vs_anxiety.png")
    plt.clf()

    corr = df.corr(numeric_only=True)
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.savefig(PLOT_DIR / "correlation_matrix.png")
    plt.clf()

    df.sort_values("Anxiety_Prevalence_%", ascending=False).head(10).to_csv(PLOT_DIR / "top10_anxiety.csv", index=False)
    df.sort_values("Light_Intensity", ascending=False).head(10).to_csv(PLOT_DIR / "top10_light.csv", index=False)

    print("✅ EDA completed and plots saved.")

if __name__ == "__main__":
    main()
