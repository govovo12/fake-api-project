# utils/logger/log_writer.py
from config.paths import LOG_PATH

def write_log(level: str, message: str):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{level}] {message}\n")

