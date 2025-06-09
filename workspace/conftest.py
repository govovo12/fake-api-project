# conftest.py
import sys
from pathlib import Path
import pytest
from config import paths

# 匯入測試 fixture 模組（修正路徑與名稱）
from utils.fixture.fixture_env import temp_env_fixture
from utils.fixture.fixture_logger import fake_logger
from utils.fixture.fixture_time import fake_now
from utils.fixture.fixture_data import fake_user_data
from utils.fixture.fixture_file import temp_file
from utils.fixture.fixture_request import fake_session
from utils.fixture.fixture_stub import stub_cart_payload
from utils.fixture.fixture_assert import fake_status_code

# 匯入 mock 工廠與控制器流程 mock 工具
from utils.mock.mock_helper import get_mock
from workspace.utils.base.base_controller_test import BaseControllerFlowMock

# 修正 sys.path（保留原本邏輯）
ROOT = Path(__file__).resolve().parents[0]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

def pytest_configure(config):
    # 新增 no_log_patch 標記支援，供 E2E 測試跳過 log patch 使用
    config.addinivalue_line("markers", "no_log_patch: skip global LOG_PATH monkeypatch")

@pytest.fixture(autouse=True)
def always_patch_log_path(request, monkeypatch, tmp_path):
    """所有測試統一打 patch，防止寫入正式 reports/run_log.txt
    可加 mark: no_log_patch 來跳過 patch
    """
    if "no_log_patch" in request.keywords:
        return  # E2E 測試跳過 patch，實際寫入正式 log

    fake_log_path = tmp_path / "run_log.txt"
    monkeypatch.setattr(paths, "LOG_PATH", fake_log_path)

# ✅ mock_factory：統一提供動態 mock 工具的 fixture
@pytest.fixture
def mock_factory():
    def _factory(name: str, *args, **kwargs):
        return get_mock(name, *args, **kwargs)
    return _factory

# ✅ controller_mock：控制器整合測試專用工具
@pytest.fixture
def controller_mock():
    """提供控制器流程模擬工具（Shopee 風格整合測試）"""
    return BaseControllerFlowMock()
