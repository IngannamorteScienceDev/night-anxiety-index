import subprocess
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
VENV_PYTHON = BASE_DIR / ".venv" / "Scripts" / "python.exe"  # для Windows
# VENV_PYTHON = BASE_DIR / ".venv" / "bin" / "python"  # для Linux/Mac

SCRIPTS = [
    "scripts/preprocess_anxiety_data.py",
    "scripts/preprocess_nightlight.py",
    "scripts/merge_datasets.py",
    "scripts/eda_main.py",
    "scripts/train_models.py",
    "scripts/visualize_models.py",
    "scripts/final_map.py"
]

def run_pipeline():
    print("🚀 Starting full pipeline...")
    for script in SCRIPTS:
        print(f"\n📄 Running: {script}")
        result = subprocess.run([str(VENV_PYTHON), script], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ Error in {script}")
            print(result.stderr)
            break
        else:
            print(f"✅ Finished: {script}")
            print(result.stdout)

    print("\n🎉 Pipeline complete!")

if __name__ == "__main__":
    run_pipeline()
