import pytest

class BaseLogTest:
    """
    測試基底類別：提供 log 捕捉與模擬工具
    """
    is_tool = True

    @pytest.fixture
    def log_capture(self):
        # 這裡可放 log capture 的 setup
        pass
