import pandas as pd
import plotly.express as px
from pathlib import Path

# Define paths to input data and output directory
DATA_PATH = Path("data/processed/anxiety_prevalence_2019.csv")
OUTPUT_PATH = Path("outputs/plots/anxiety_map.png")

# Ensure the output directory exists
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

def main():
    # Step 1: Load the processed anxiety prevalence dataset
    df = pd.read_csv(DATA_PATH)

    # Step 2: Create a choropleth map using Plotly Express
    fig = px.choropleth(
        df,
        locations="Country_Code",  # ISO alpha-3 country codes
        color="Anxiety_Prevalence_%",  # Color intensity based on prevalence
        hover_name="Country",  # Country name on hover
        color_continuous_scale="OrRd",  # Orange-Red color scale
        range_color=(df["Anxiety_Prevalence_%"].min(), df["Anxiety_Prevalence_%"].max()),
        title="Anxiety Prevalence by Country (2019)",
        labels={"Anxiety_Prevalence_%": "Prevalence (%)"}
    )

    # Step 3: Update layout for cleaner appearance
    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=False),
        title_x=0.5,  # Center the title
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    # Step 4: Display the interactive map in the browser
    fig.show()

    # Step 5: Try to save the figure as a static PNG image
    try:
        fig.write_image(str(OUTPUT_PATH), width=1200, height=600)
        print(f"Static map saved to: {OUTPUT_PATH}")
    except Exception as e:
        print("Could not save static image.")
        print("Reason:", e)
        print("Hint: Install the 'kaleido' library with: pip install -U kaleido")

if __name__ == "__main__":
    main()
