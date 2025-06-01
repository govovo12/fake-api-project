import pytest

class BaseDataTest:
    """
    測試基底類別：提供資料準備與清理 fixture
    """
    is_tool = True

    @pytest.fixture
    def sample_data(self):
        return {"key": "value"}
