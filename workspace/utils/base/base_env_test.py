import pytest

class BaseEnvTest:
    """
    測試基底類別：提供環境變數與設定相關 fixture
    """
    is_tool = True

    @pytest.fixture
    def env_setup(self, monkeypatch):
        monkeypatch.setenv("FAKE_ENV", "test")
