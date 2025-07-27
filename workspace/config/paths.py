from pathlib import Path
import json
from workspace.utils.env.env_manager import get_env

# === 專案根目錄與 workspace 根路徑 ===

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
WORKSPACE_ROOT = PROJECT_ROOT / "workspace"

# === 測試資料目錄 ===

TESTDATA_ROOT = WORKSPACE_ROOT / "testdata"
USER_TESTDATA_DIR = TESTDATA_ROOT / "user"
PRODUCT_TESTDATA_DIR = TESTDATA_ROOT / "product"

def get_user_path(uuid: str) -> Path:
    """根據 UUID 取得 user 測資 JSON 路徑"""
    return USER_TESTDATA_DIR / f"{uuid}.json"

def get_product_path(uuid: str) -> Path:
    """根據 UUID 取得 product 測資 JSON 路徑"""
    return PRODUCT_TESTDATA_DIR / f"{uuid}.json"
def get_cart_path(uuid: str) -> Path:
    """根據 UUID 取得 cart 測資 JSON 路徑"""
    return Path(f"workspace/testdata/cart/{uuid}.json")

def get_user_testdata_path(filename: str) -> Path:
    return USER_TESTDATA_DIR / filename

def get_product_testdata_path(filename: str) -> Path:
    return PRODUCT_TESTDATA_DIR / filename
def get_create_product_url() -> str:
    """取得建立商品 API 的完整 URL"""
    return f"{get_base_url()}{get_env('FAKESTORE_PRODUCT_PATH')}"
def get_create_cart_url() -> str:
    """取得建立購物車 API 的完整 URL"""
    return f"{get_base_url()}{get_env('FAKESTORE_CART_PATH')}"

# === 測試模組路徑 ===

TESTS_ROOT = WORKSPACE_ROOT / "tests"
UNIT_TESTS_ROOT = TESTS_ROOT / "unit"
INTEGRATION_TESTS_ROOT = TESTS_ROOT / "integration"

# === 環境變數與 API 設定 ===

def get_headers() -> dict:
    """從環境變數取得 API headers"""
    try:
        return json.loads(get_env("FAKESTORE_HEADERS"))
    except Exception:
        return {}

def get_base_url() -> str:
    return get_env("FAKESTORE_BASE_URL")

def get_register_url() -> str:
    return f"{get_base_url()}{get_env('FAKESTORE_REGISTER_PATH')}"

def get_login_url() -> str:
    return f"{get_base_url()}{get_env('FAKESTORE_LOGIN_PATH')}"

# === 暫時保留 log 寫入位置（供測試 monkeypatch 用） ===
LOG_PATH = WORKSPACE_ROOT / "reports" / "run_log.txt"

# === 主控e2e測試時使用===
def get_project_root() -> Path:
    """
    ✅ 傳回整個 fake-api-project 專案根目錄。
    """
    return Path(__file__).resolve().parents[2]
def get_env_path() -> Path:
    """
    ✅ 傳回 fake-api-project 根目錄下的 .env 絕對路徑。
    """
    return PROJECT_ROOT / ".env"

# 專案根目錄（BASE_DIR = workspace 的上一層）
BASE_DIR = Path(__file__).resolve().parent.parent.parent

def get_report_dir():
    """取得 pytest 報告的根目錄（HTML 專用）"""
    return BASE_DIR / "workspace" / "reports"

def get_html_report_path(filename: str = "test_report.html"):
    """
    取得 HTML 報告完整路徑（可帶自訂檔名）
    :param filename: 預設為 test_report.html，可改為帶 timestamp 的名稱
    :return: reports/ 下的完整報告路徑
    """
    return get_report_dir() / filename

def get_phase_report_dir(phase: str) -> Path:
    """取得指定測試階段（unit/integration/e2e/infra）的報告資料夾"""
    return get_report_dir() / phase

def get_phase_coverage_dir(phase: str) -> Path:
    """取得指定測試階段的 coverage 輸出資料夾"""
    return get_report_dir() / "coverage" / phase

def get_htmlcov_dir() -> Path:
    return get_report_dir() / "coverage"

def get_phase_test_dir(phase: str) -> Path:
    """
    根據測試階段回傳對應測試目錄
    - unit → workspace/tests/unit
    - infra → workspace/tests/infra
    - integration → workspace/tests/integration
    - e2e → workspace/tests/e2e
    """
    return TESTS_ROOT / phase
