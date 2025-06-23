# conftest.py
import sys
import pytest
from pathlib import Path
from config import paths  # 正確 patch 目標是這個 paths

# ✅ 匯入測試 fixture 模組（修正路徑與名稱）
from utils.fixture.fixture_env import temp_env_fixture
from utils.fixture.fixture_logger import fake_logger
from utils.fixture.fixture_time import fake_now
from utils.fixture.fixture_data import fake_user_data
from utils.fixture.fixture_file import temp_file
from utils.fixture.fixture_request import fake_session
from utils.fixture.fixture_stub import stub_cart_payload
from utils.fixture.fixture_assert import fake_status_code

# ✅ 匯入 mock 工具與整體流程 mock 工具
from utils.mock.mock_helper import get_mock
from workspace.utils.base.base_controller_test import BaseControllerFlowMock

# ✅ 修正 sys.path（保留原本邏輯）
ROOT = Path(__file__).resolve().parents[0]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

def pytest_configure(config):
    """
    pytest 啟動時載入額外標記設定
    - 新增 no_log_patch 標記，讓某些測試禁用 LOG_PATH patch（例如 E2E 測試）
    """
    config.addinivalue_line("markers", "no_log_patch: skip global LOG_PATH monkeypatch")

# ✅ log patch（所有測試統一 patch，除非加上 no_log_patch）
@pytest.fixture(autouse=True)
def always_patch_log_path(request, monkeypatch, tmp_path):
    """
    預設將 log 輸出路徑指向 temp_path 下的 run_log.txt
    如需略過請加上 pytest.mark.no_log_patch
    """
    if "no_log_patch" in request.keywords:
        return

    fake_log_path = tmp_path / "run_log.txt"
    monkeypatch.setattr(paths, "LOG_PATH", fake_log_path)

# ✅ 提供統一 mock 工具的 fixture
@pytest.fixture
def mock_factory():
    def _factory(name: str, *args, **kwargs):
        return get_mock(name, *args, **kwargs)
    return _factory

# ✅ 控管整體流程的 mock 工具
@pytest.fixture
def controller_mock():
    """提供 Shopee 類整體流程 mock 工具"""
    return BaseControllerFlowMock()
