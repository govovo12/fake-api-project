# workspace/tests/fixtures/controller_fixtures.py

import pytest
from workspace.config.paths import (
    get_env_path,
    get_register_url,
    get_headers,
)
from workspace.utils.env.env_manager import load_env, get_env


@pytest.fixture(scope="session")
def env_loaded() -> bool:
    """
    ✅ 載入 .env 檔案
    """
    env_path = get_env_path()
    if not load_env(env_path):
        raise FileNotFoundError(f"❌ 無法載入 .env，路徑: {env_path}")
    return True


@pytest.fixture(scope="session")
def headers(env_loaded) -> dict:
    """
    ✅ 載入 headers 設定
    """
    return get_headers()


@pytest.fixture(scope="session")
def url(env_loaded) -> str:
    """
    ✅ 主控需要的是完整註冊 URL（含 /users）
    """
    return get_register_url()


@pytest.fixture(scope="session")
def login_cred(env_loaded) -> dict:
    """
    ✅ 登入／註冊需要的帳密資訊
    """
    return {
        "username": get_env("FAKESTORE_LOGIN_USERNAME"),
        "password": get_env("FAKESTORE_LOGIN_PASSWORD"),
    }


@pytest.fixture(scope="session")
def controller_inputs(headers, url, login_cred) -> tuple:
    """
    ✅ 提供主控所需的三大輸入：headers, 註冊 URL, 帳密
    """
    return headers, url, login_cred
