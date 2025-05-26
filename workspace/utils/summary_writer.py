import re
import time
from pathlib import Path

log_path = Path("workspace/reports/run_log.txt")
summary_lines = []

unit_count = 0
unit_passed = 0
int_count = 0
int_passed = 0
failures = 0

if not log_path.exists():
    print("[Summary] No run_log.txt found.")
    exit(1)

with log_path.open(encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()
    in_unit = False
    in_integration = False
    for i, line in enumerate(lines):
        if "===== UNIT TEST STARTED" in line:
            in_unit = True
            in_integration = False
        elif "===== INTEGRATION TEST STARTED" in line:
            in_unit = False
            in_integration = True

        if in_unit:
            if re.search(r"::.*PASSED", line):
                unit_passed += 1
                unit_count += 1
            elif re.search(r"::.*FAILED", line):
                unit_count += 1
                failures += 1

        elif in_integration:
            if "PASSED" in line and not any(tag in line for tag in ["[INFO]", "INFO  -"]):
                int_passed += 1
                int_count += 1
            elif "FAILED" in line and not any(tag in line for tag in ["[INFO]", "INFO  -"]):
                int_count += 1
                failures += 1

summary_lines.append("\n=== Test Summary ===")
summary_lines.append(f"[Unit Tests]      {unit_passed} / {unit_count} passed")
summary_lines.append(f"[Integration]     {int_passed} / {int_count} passed")
summary_lines.append(f"[Failures]        {failures}")
summary_lines.append("[Reports]")
summary_lines.append(" - unit_report.html")
summary_lines.append(" - integration_report.html")

# Retry writing to log file
for _ in range(3):
    try:
        with log_path.open("a", encoding="utf-8") as f:
            f.write("\n" + "\n".join(summary_lines) + "\n")
        print("[Summary] Summary written to run_log.txt")
        break
    except PermissionError:
        print("[Summary] ERROR - Could not write to run_log.txt (file locked)")
        time.sleep(1)
else:
    print("[Summary] ERROR - Failed to write to run_log.txt after multiple attempts")
