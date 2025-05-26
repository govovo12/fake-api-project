import sys

with open("workspace/reports/run_log.txt", "w", encoding="utf-8") as f:
    for line in sys.stdin:
        print(line, end="")  # 也印到螢幕
        f.write(line)
