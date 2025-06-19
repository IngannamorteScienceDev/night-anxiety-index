import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Define base directories and paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data/processed/df_model.csv"
PLOT_DIR = BASE_DIR / "outputs/plots"

# Ensure plot output directory exists
PLOT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    # Step 1: Load merged dataset
    df = pd.read_csv(DATA_PATH)

    # Step 2: Print summary statistics
    print("Descriptive statistics:")
    print(df.describe())

    # Step 3: Print Pearson correlation matrix for numeric columns
    print("Pearson correlation:")
    print(df.corr(numeric_only=True))

    # Step 4: Plot histogram of anxiety prevalence
    sns.histplot(df["Anxiety_Prevalence_%"], kde=True)
    plt.title("Distribution of Anxiety Prevalence (%)")
    plt.xlabel("Anxiety Prevalence (%)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "hist_anxiety.png")
    plt.clf()

    # Step 5: Plot histogram of light intensity (log scale)
    sns.histplot(df["Light_Intensity"], kde=True)
    plt.title("Distribution of Light Intensity")
    plt.xlabel("Light Intensity (raw)")
    plt.xscale("log")
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "hist_light.png")
    plt.clf()

    # Step 6: Scatterplot: Light Intensity vs. Anxiety Prevalence
    sns.scatterplot(x="Light_Intensity", y="Anxiety_Prevalence_%", data=df)
    plt.xscale("log")
    plt.title("Anxiety Prevalence vs Light Intensity")
    plt.xlabel("Light Intensity (log scale)")
    plt.ylabel("Anxiety Prevalence (%)")
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "scatter_light_vs_anxiety.png")
    plt.clf()

    # Step 7: Heatmap of correlation matrix
    corr = df.corr(numeric_only=True)
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.savefig(PLOT_DIR / "correlation_matrix.png")
    plt.clf()

    # Step 8: Save top 10 countries by anxiety and light intensity
    df.sort_values("Anxiety_Prevalence_%", ascending=False).head(10).to_csv(
        PLOT_DIR / "top10_anxiety.csv", index=False
    )
    df.sort_values("Light_Intensity", ascending=False).head(10).to_csv(
        PLOT_DIR / "top10_light.csv", index=False
    )

    print("EDA completed successfully. Plots and summary files saved.")

if __name__ == "__main__":
    main()
