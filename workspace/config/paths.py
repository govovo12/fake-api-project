from pathlib import Path
from workspace.utils.env.env_manager import EnvManager

# === 基礎路徑定義 ===

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
WORKSPACE_ROOT = PROJECT_ROOT / "workspace"

# === utils 模組資料夾 ===
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
UUID_ROOT = UTILS_ROOT / "uuid"
UUID_GENERATOR_PATH = UUID_ROOT / "uuid_generator.py"

# === 任務模組資料夾 ===
TASKS_ROOT = WORKSPACE_ROOT / "modules" / "tasks"

# === 測試資料夾 (testdata) ===
TESTDATA_ROOT = WORKSPACE_ROOT / "testdata"

USER_TESTDATA_DIR = TESTDATA_ROOT / "user"
PRODUCT_TESTDATA_DIR = TESTDATA_ROOT / "product"
ORDER_TESTDATA_DIR = TESTDATA_ROOT / "order"      # 可預留
CART_TESTDATA_DIR = TESTDATA_ROOT / "cart"        # 可預留

# ✅ 測資檔案路徑（依 uuid 命名）
def get_user_path(uuid: str) -> Path:
    """根據 UUID 取得 user 測資 JSON 路徑"""
    return USER_TESTDATA_DIR / f"{uuid}.json"

def get_product_path(uuid: str) -> Path:
    """根據 UUID 取得 product 測資 JSON 路徑"""
    return PRODUCT_TESTDATA_DIR / f"{uuid}.json"

# ✅ 直接指定檔名（額外載入特定檔案）
def get_user_testdata_path(filename: str) -> Path:
    return USER_TESTDATA_DIR / filename

def get_product_testdata_path(filename: str) -> Path:
    return PRODUCT_TESTDATA_DIR / filename

# === config 路徑 ===
CONFIG_ROOT = WORKSPACE_ROOT / "config"
ENVS_CONFIG_ROOT = CONFIG_ROOT / "envs"

FAKE_PRODUCT_CONFIG_PATH = ENVS_CONFIG_ROOT / "fake_product_config.py"
FAKE_USER_CONFIG_PATH = ENVS_CONFIG_ROOT / "fake_user_config.py"
LOGIN_ENV_PATH = ENVS_CONFIG_ROOT / "api.env"

def get_env_config_path(filename: str) -> Path:
    return ENVS_CONFIG_ROOT / filename

# === 測試模組 ===
TESTS_ROOT = WORKSPACE_ROOT / "tests"
UNIT_TESTS_ROOT = TESTS_ROOT / "unit"
INTEGRATION_TESTS_ROOT = TESTS_ROOT / "integration"

# === 日誌與暫存區 ===
LOGS_ROOT = PROJECT_ROOT / "logs"
TMP_ROOT = PROJECT_ROOT / "tmp"
LOG_PATH = WORKSPACE_ROOT / "reports" / "run_log.txt"

# === 模組路徑查詢工具 ===
def get_module_path(mod_name: str) -> Path:
    return UTILS_ROOT / mod_name

def get_task_module_path(task_name: str) -> Path:
    return TASKS_ROOT / f"{task_name}.py"

def get_unit_test_path(module: str) -> Path:
    return UNIT_TESTS_ROOT / module

def get_integration_test_path(module: str) -> Path:
    return INTEGRATION_TESTS_ROOT / module

# ✅ API 端點（從 env 載入）
API_ENV_PATH = get_env_config_path("api.env")
_api_env = EnvManager.load_env_dict(API_ENV_PATH)

REGISTER_ENDPOINT = _api_env.get("REGISTER_URL", "https://fakestoreapi.com/users")
LOGIN_ENDPOINT = _api_env.get("LOGIN_URL", "https://fakestoreapi.com/auth/login")
