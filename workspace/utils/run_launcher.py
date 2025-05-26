# === 確保 workspace 為 PYTHONPATH 根目錄（支援本機與 CI）===
import sys
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[2]
if str(ROOT_PATH) not in sys.path:
    sys.path.insert(0, str(ROOT_PATH))

import subprocess
from datetime import datetime

BASE_DIR = ROOT_PATH
REPORT_DIR = BASE_DIR / "workspace" / "reports"
LOG_PATH = REPORT_DIR / "run_log.txt"
UNIT_TESTS = BASE_DIR / "workspace" / "tests" / "unit"
INTEGRATION_TESTS = BASE_DIR / "workspace" / "tests" / "integration"
SUMMARY_WRITER = BASE_DIR / "workspace" / "utils" / "summary_writer.py"
PYTHON_EXE = BASE_DIR / "venv" / "Scripts" / "python.exe"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


def run_pytest(label, test_path, report_name):
    print(f"[TEST] Running {label} tests...")
    report_path = REPORT_DIR / report_name

    result = subprocess.run([
        str(PYTHON_EXE), "-m", "pytest", "-v", "--color=no", "--capture=tee-sys",
        str(test_path),
        f"--html={report_path}",
        "--self-contained-html"
    ], cwd=str(BASE_DIR), capture_output=True, text=True, encoding="utf-8", errors="ignore")

    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write(f"\n===== {label.upper()} TEST STARTED @ {datetime.now()} =====\n")
        log_file.write(result.stdout)
        log_file.write(result.stderr)

    if result.returncode != 0:
        print(f"[FAIL] {label} tests failed. See log.")
        return False

    print(f"[PASS] {label} tests passed.")
    return True


def main():
    LOG_PATH.write_text("", encoding="utf-8")

    unit_ok = run_pytest("unit", UNIT_TESTS, "unit_report.html")
    if not unit_ok:
        return

    integration_ok = run_pytest("integration", INTEGRATION_TESTS, "integration_report.html")
    if not integration_ok:
        return

    print("[INFO] Writing summary...")
    subprocess.run([str(PYTHON_EXE), str(SUMMARY_WRITER)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    print("[DONE] All tests completed successfully.")


if __name__ == "__main__":
    main()
