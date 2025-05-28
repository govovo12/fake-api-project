from pathlib import Path

# === 基準定位：專案根目錄 ===
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# === 常用子資料夾 ===
WORKSPACE_ROOT = PROJECT_ROOT / "workspace"
TESTS_ROOT = WORKSPACE_ROOT / "tests"
TESTDATA_PATH = WORKSPACE_ROOT / "testdata"
REPORT_PATH = WORKSPACE_ROOT / "reports"
CONFIG_PATH = WORKSPACE_ROOT / "config"

# === utils 子模組 ===
UTILS_PATH = WORKSPACE_ROOT / "utils"
TIME_UTILS_PATH = UTILS_PATH / "time"
ASSERT_UTILS_PATH = UTILS_PATH / "asserts"
FILE_UTILS_PATH = UTILS_PATH / "file"
CALLBACK_UTILS_PATH = UTILS_PATH / "callback"
EXPORT_UTILS_PATH = UTILS_PATH / "export"

# === 測試子模組 ===
UNIT_TESTS_PATH = TESTS_ROOT / "unit"
TIME_UNIT_TEST_PATH = UNIT_TESTS_PATH / "time"

# === 常用函式 ===
def get_account_json_path(filename: str) -> Path:
    return TESTDATA_PATH / "account" / filename

# === 預設帳號資料檔案 ===
DEFAULT_ACCOUNT_FILENAME = "valid_case.json"
def get_account_json_path(filename: str) -> Path:
    return TESTDATA_PATH / "account" / filename

def get_default_account_json_path() -> Path:
    return get_account_json_path(DEFAULT_ACCOUNT_FILENAME)

# === 常用檔案 ===
ACCOUNT_REPORT_PATH = REPORT_PATH / "account_generator_report.html"
LOG_PATH = REPORT_PATH / "run_log.txt"

# === .env 設定檔 ===
ENV_PATH = CONFIG_PATH / "envs"
ACCOUNT_ENV_PATH = ENV_PATH / "account_gen.env"
LOGIN_ENV_PATH = ENV_PATH / "login.env"
