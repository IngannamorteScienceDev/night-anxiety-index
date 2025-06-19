import subprocess
import os
import sys
import platform
import re
import shutil
from tqdm import tqdm
from datetime import datetime

# === Scripts to run ===
SCRIPTS = [
    "scripts/preprocess_anxiety_data.py",
    "scripts/preprocess_nightlight.py",
    "scripts/merge_datasets.py",
    "scripts/eda_main.py",
    "scripts/train_models.py",
    "scripts/visualize_models.py",
    "scripts/final_map.py"
]

# === Folders to clean ===
FOLDERS_TO_CLEAN = [
    "data/processed",
    "models",
    "outputs/reports",
    "outputs/plots"
]

# === Emoji stripping on broken Windows encoding ===
CLEAN_OUTPUT = (platform.system() == "Windows" and (sys.stdout.encoding or '').lower() != "utf-8")

# === Dynamic log filename ===
now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"pipeline_{now_str}.log")

def clean_text(text: str) -> str:
    """Remove emojis if terminal encoding is broken."""
    if CLEAN_OUTPUT:
        return re.sub(r'[^\x00-\x7F]+', '', text)
    return text

def log_write(message: str):
    """Append message to log file (UTF-8)."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def init_log():
    """Start new log file with header."""
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"🕒 Pipeline started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n")

def clean_directories():
    """Remove previous generated files from selected folders."""
    print(clean_text("🧹 Cleaning previous outputs..."))
    log_write("🧹 Cleaning previous outputs...")
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
                    msg = f"⚠️ Failed to delete {file_path}: {e}"
                    print(clean_text(msg))
                    log_write(msg)
    print(clean_text("✅ Cleanup complete.\n"))
    log_write("✅ Cleanup complete.\n")

def run_script(script_path: str):
    """Run one script and log output/errors."""
    header = f"\n📄 Running: {script_path}"
    print(clean_text(header))
    log_write(header)

    result = subprocess.run(
        [sys.executable, script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode == 0:
        msg = f"✅ Finished: {script_path}"
        print(clean_text(msg))
        log_write(msg)
        log_write("▶ Output:\n" + result.stdout.strip())
    else:
        err = f"❌ Error in {script_path}"
        print(clean_text(err))
        log_write(err)
        log_write("💥 Error output:\n" + result.stderr.strip())

def main():
    """Main controller."""
    print(clean_text("🚀 Starting full pipeline...\n"))
    init_log()
    clean_directories()

    for script in tqdm(SCRIPTS, desc=clean_text("🧠 Running scripts"), ncols=80, colour="green"):
        run_script(script)

    final_msg = "\n🎉 Pipeline complete!"
    print(clean_text(final_msg))
    log_write(final_msg)

if __name__ == "__main__":
    main()
