import pytest
from unittest.mock import patch

class BaseTimeTest:
    """
    測試基底類別：提供時間控制與 patch 工具
    """
    is_tool = True

    @pytest.fixture
    def freeze_time(self):
        with patch("time.time") as mock_time:
            mock_time.return_value = 1234567890
            yield mock_time
