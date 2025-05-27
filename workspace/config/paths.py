from pathlib import Path

# === 基準定位：專案根目錄 ===
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# === 常用子資料夾 ===
WORKSPACE_ROOT = PROJECT_ROOT / "workspace"
TESTS_ROOT = WORKSPACE_ROOT / "tests"
TESTDATA_PATH = WORKSPACE_ROOT / "testdata"
REPORT_PATH = WORKSPACE_ROOT / "reports"
CONFIG_PATH = WORKSPACE_ROOT / "config"


# === 常用檔案 ===
ACCOUNT_GEN_DATA_JSON = TESTDATA_PATH / "login" / "valid_case.json"
ACCOUNT_REPORT_PATH = REPORT_PATH / "account_generator_report.html"
LOG_PATH = REPORT_PATH / "run_log.txt"


# === .env 設定檔 ===
ENV_PATH = CONFIG_PATH / "envs"
ACCOUNT_ENV_PATH = ENV_PATH / "account_gen.env"
LOGIN_ENV_PATH = ENV_PATH / "login.env"
