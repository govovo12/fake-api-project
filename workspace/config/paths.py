from pathlib import Path
from workspace.utils.env.env_manager import EnvManager

# Fake-API 專案根目錄 (config 同層往上兩層)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

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
UUID_ROOT = UTILS_ROOT / "uuid"
UUID_GENERATOR_PATH = UUID_ROOT / "uuid_generator.py"

# 任務模組資料夾
TASKS_ROOT = WORKSPACE_ROOT / "modules" / "tasks"  # 建議存放控制器、任務模組

# 測試資料（testdata）資料夾
TESTDATA_ROOT = WORKSPACE_ROOT / "testdata"
USER_TESTDATA_ROOT = TESTDATA_ROOT / "user"
PRODUCT_TESTDATA_ROOT = TESTDATA_ROOT / "product"
ORDER_TESTDATA_ROOT = TESTDATA_ROOT / "order"        # 可預留
CART_TESTDATA_ROOT = TESTDATA_ROOT / "cart"          # 可預留

def get_user_testdata_path(filename: str) -> Path:
    return USER_TESTDATA_ROOT / filename

def get_product_testdata_path(filename: str) -> Path:
    return PRODUCT_TESTDATA_ROOT / filename

def get_order_testdata_path(filename: str) -> Path:
    return ORDER_TESTDATA_ROOT / filename

def get_cart_testdata_path(filename: str) -> Path:
    return CART_TESTDATA_ROOT / filename

# config 路徑
CONFIG_ROOT = WORKSPACE_ROOT / "config"
ENVS_CONFIG_ROOT = CONFIG_ROOT / "envs"
FAKE_PRODUCT_CONFIG_PATH = ENVS_CONFIG_ROOT / "fake_product_config.py"
FAKE_USER_CONFIG_PATH = ENVS_CONFIG_ROOT / "fake_user_config.py"  # 未來有 user config 可預留
LOGIN_ENV_PATH = ENVS_CONFIG_ROOT / "api.env"

def get_env_config_path(filename: str) -> Path:
    """取得 envs 目錄下的設定檔完整路徑"""
    return ENVS_CONFIG_ROOT / filename

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

# ✅ API 端點設定（由 api.env 提供）
API_ENV_PATH = get_env_config_path("api.env")
_api_env = EnvManager.load_env_dict(API_ENV_PATH)

REGISTER_ENDPOINT = _api_env.get("REGISTER_URL", "https://fakestoreapi.com/users")
LOGIN_ENDPOINT = _api_env.get("LOGIN_URL", "https://fakestoreapi.com/auth/login")
