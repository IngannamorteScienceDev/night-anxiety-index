import subprocess
import os
import sys
import platform
import re

SCRIPTS = [
    "scripts/preprocess_anxiety_data.py",
    "scripts/preprocess_nightlight.py",
    "scripts/merge_datasets.py",
    "scripts/eda_main.py",
    "scripts/train_models.py",
    "scripts/visualize_models.py",
    "scripts/final_map.py"
]

CLEAN_OUTPUT = (platform.system() == "Windows" and sys.stdout.encoding.lower() != "utf-8")

def clean_text(text):
    if CLEAN_OUTPUT:
        return re.sub(r'[^\x00-\x7F]+', '', text)
    return text

def run_script(script_path):
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
    print(clean_text("🚀 Starting full pipeline..."))
    for script in SCRIPTS:
        run_script(script)
    print(clean_text("\n🎉 Pipeline complete!"))

if __name__ == "__main__":
    main()
