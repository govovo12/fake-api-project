"""
📦 測試批次執行腳本：依序執行四階段測試、產出報告、計算覆蓋率
"""

import sys
import os
import subprocess
from pathlib import Path

# ✅ 設定專案根目錄
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

# ✅ 匯入自訂模組
from workspace.scripts.report_setup import (
    reset_report_root,
    get_timestamped_report_path,
    get_coverage_output_path,
    generate_index_html,
    combine_coverage_reports,
)
from workspace.config.paths import get_phase_test_dir


# ✅ 測試階段設定（順序不可變）
TEST_PHASES = [
    ("unit", "unit"),
    ("infra", "infra"),
    ("integration", "integration"),
    ("e2e", "e2e"),
]


def run_pytest_with_coverage(marker: str, phase: str) -> int:
    """
    執行指定測試階段，產生測試 HTML + 對應 coverage
    """
    report_path = get_timestamped_report_path(phase)
    coverage_dir = get_coverage_output_path(phase)
    cov_target = get_phase_test_dir(phase)

    print(f"\n🚀 執行 [{phase}] 測試")
    print(f"📄 測試報告輸出：{report_path}")
    print(f"📈 覆蓋率輸出：{coverage_dir}")

    command = [
        sys.executable, "-m", "pytest",
        "-m", marker,
        "-v", "--tb=short", "--capture=no",
        f"--html={report_path}", "--self-contained-html",
        f"--cov={cov_target}", f"--cov-report=html:{coverage_dir}",
        f"--cov-config=.coveragerc",
        f"--cov-append",
                ]

    # ✅ 每個階段覆蓋率單獨存檔（讓 combine 使用）
    env = dict(**os.environ, COVERAGE_FILE=str(coverage_dir.parent / f".coverage.{phase}"))
    result = subprocess.run(command, cwd=BASE_DIR, env=env)
    return result.returncode


def main():
    print("\n🚀 開始執行完整測試流程...\n")
    reset_report_root()

    for marker, phase in TEST_PHASES:
        result_code = run_pytest_with_coverage(marker, phase)
        if result_code != 0:
            print(f"\n❌ [{phase}] 測試失敗，流程中止")
            sys.exit(result_code)

    print("\n📊 合併所有 coverage 檔案中...")
    combine_coverage_reports()
    print("📊 合併完成，總體報告位於：workspace/reports/coverage/total/index.html")

    generate_index_html()
    print("\n✅ 所有測試完成，報告已產出於 workspace/reports/ 下\n")



if __name__ == "__main__":
    main()
