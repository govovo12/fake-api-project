import pytest

class BaseAssertTest:
    """
    測試基底類別：提供 assert helper，供各測試繼承使用
    """
    is_tool = True  # tools table 掃描用

    @pytest.fixture(autouse=True)
    def setup(self):
        # 這裡放共用前置，視需要調整
        pass

    def assert_success(self, result):
        assert result is True

    def assert_fail(self, result):
        assert result is False
