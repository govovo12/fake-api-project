from pathlib import Path

# Fake-API 專案根目錄 (config 同層往上兩層)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# workspace 根目錄
WORKSPACE_ROOT = PROJECT_ROOT / "workspace"

# 各主要 utils 模組資料夾
UTILS_ROOT = WORKSPACE_ROOT / "utils"
LOGGER_ROOT = UTILS_ROOT / "logger"
NOTIFIER_ROOT = UTILS_ROOT / "notifier"
RETRY_ROOT = UTILS_ROOT / "retry"
REQUEST_ROOT = UTILS_ROOT / "request"
FILE_ROOT = UTILS_ROOT / "file"
ENV_ROOT = UTILS_ROOT / "env"
MOCK_ROOT = UTILS_ROOT / "mock"
FIXTURE_ROOT = UTILS_ROOT / "fixture"
TIME_ROOT = UTILS_ROOT / "time"
STUB_ROOT = UTILS_ROOT / "stub"
EXPORT_ROOT = UTILS_ROOT / "export"
CALLBACK_ROOT = UTILS_ROOT / "callback"
ASSERT_ROOT = UTILS_ROOT / "asserts"
FAKE_ROOT = UTILS_ROOT / "fake"
DATA_ROOT = UTILS_ROOT / "data"

# 任務模組資料夾（如自動打卡）
TASKS_ROOT = WORKSPACE_ROOT / "task"

# 測試資料夾
TESTS_ROOT = WORKSPACE_ROOT / "tests"
UNIT_TESTS_ROOT = TESTS_ROOT / "unit"
INTEGRATION_TESTS_ROOT = TESTS_ROOT / "integration"

# 日誌與暫存資料夾
LOGS_ROOT = PROJECT_ROOT / "logs"
TMP_ROOT = PROJECT_ROOT / "tmp"

# log 檔案路徑，conftest.py 會 patch 它
LOG_PATH = WORKSPACE_ROOT / "reports" / "run_log.txt"

# 取得指定模組的工具檔案路徑（例如 utils/logger）
def get_module_path(mod_name: str) -> Path:
    return UTILS_ROOT / mod_name

# 取得指定任務模組路徑（例如 task_login.py）
def get_task_module_path(task_name: str) -> Path:
    return TASKS_ROOT / f"{task_name}.py"

# 取得單元測試資料夾下模組路徑（方便統一管理）
def get_unit_test_path(module: str) -> Path:
    return UNIT_TESTS_ROOT / module

# 取得整合測試資料夾下模組路徑
def get_integration_test_path(module: str) -> Path:
    return INTEGRATION_TESTS_ROOT / module
