"""
測試批次執行腳本（使用 subprocess 呼叫 pytest CLI）
每組測試獨立產出 HTML 報告，放入 workspace/reports
"""

import sys
import subprocess
from pathlib import Path

# ✅ 插入 workspace 專案根目錄（scripts 的上上層）
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

# ✅ 現在才 import 其他模組（必須在 sys.path 設定之後）
from workspace.scripts.report_setup import get_timestamped_report_path
import pytest


# ✅ 測試階段與標記
TEST_PHASES = [
    ("infra", "infra"),
    ("unit", "unit"),
    ("integration", "integration"),
    ("e2e", "e2e"),
]


def run_pytest_subprocess(marker: str, phase: str) -> int:
    """
    使用 subprocess 執行 pytest CLI，避免 pytest.main() 的副作用
    """
    report_path = get_timestamped_report_path(phase)
    print(f"\n📄 [{phase}] 產出報告：{report_path}")

    # CLI 執行命令
    command = [
        sys.executable, "-m", "pytest",
        "-m", marker,
        "-v", "--tb=short",
        "--capture=no",
        f"--html={report_path}",
        "--self-contained-html"
    ]

    # ✅ 呼叫子行程，接收結果
    result = subprocess.run(command, cwd=BASE_DIR)
    return result.returncode


def main():
    print("\n🚀 開始執行測試流程...\n")
    for marker, phase in TEST_PHASES:
        result_code = run_pytest_subprocess(marker, phase)
        if result_code != 0:
            print(f"\n❌ [{phase}] 測試失敗，流程中止")
            sys.exit(result_code)

    print("\n✅ 所有測試階段完成，請至 workspace/reports 查看報告\n")


if __name__ == "__main__":
    main()
