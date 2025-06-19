import subprocess
import os
import sys
import platform
import re
import shutil
from tqdm import tqdm

# === List of scripts to run in order ===
SCRIPTS = [
    "scripts/preprocess_anxiety_data.py",
    "scripts/preprocess_nightlight.py",
    "scripts/merge_datasets.py",
    "scripts/eda_main.py",
    "scripts/train_models.py",
    "scripts/visualize_models.py",
    "scripts/final_map.py"
]

# === Folders to clear before pipeline run (but NOT data/raw) ===
FOLDERS_TO_CLEAN = [
    "data/processed",
    "models",
    "outputs/reports",
    "outputs/plots"
]

# === Detect if terminal is not UTF-8 compatible (e.g. cp1251 on Windows) ===
CLEAN_OUTPUT = (platform.system() == "Windows" and (sys.stdout.encoding or '').lower() != "utf-8")

def clean_text(text: str) -> str:
    """
    Remove emojis and non-ASCII characters if terminal does not support them.
    """
    if CLEAN_OUTPUT:
        return re.sub(r'[^\x00-\x7F]+', '', text)
    return text

def clean_directories():
    """
    Clear old generated data (models, reports, processed files, plots).
    Keep raw datasets untouched.
    """
    print(clean_text("🧹 Cleaning previous outputs..."))
    for folder in FOLDERS_TO_CLEAN:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(clean_text(f"⚠️ Failed to delete {file_path}: {e}"))
    print(clean_text("✅ Cleanup complete.\n"))

def run_script(script_path: str):
    """
    Run a single Python script as subprocess and show output clearly.
    """
    print(clean_text(f"\n📄 Running: {script_path}"))
    result = subprocess.run(
        [sys.executable, script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode == 0:
        print(clean_text(f"✅ Finished: {script_path}"))
        print(clean_text(result.stdout))
    else:
        print(clean_text(f"❌ Error in {script_path}"))
        print(clean_text(result.stderr))

def main():
    """
    Run the full pipeline in sequence with a progress bar and clear logs.
    """
    print(clean_text("🚀 Starting full pipeline...\n"))
    clean_directories()

    for script in tqdm(SCRIPTS, desc=clean_text("🧠 Running scripts"), ncols=80, colour="green"):
        run_script(script)

    print(clean_text("\n🎉 Pipeline complete! All steps finished successfully."))

if __name__ == "__main__":
    main()
