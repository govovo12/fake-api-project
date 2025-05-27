import sys
from config.paths import LOG_PATH

with open(LOG_PATH, "w", encoding="utf-8") as f:
    for line in sys.stdin:
        print(line, end="")  # 也印到螢幕
        f.write(line)
