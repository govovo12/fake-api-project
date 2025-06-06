import pytest
from workspace.utils.uuid.uuid_checker import check_if_testdata_exists
from workspace.utils.file import file_helper
from pathlib import Path
pytestmark = [pytest.mark.unit, pytest.mark.uuid]

@pytest.mark.parametrize("user_exists, user_empty, product_exists, product_empty, expected", [
    (True, False, True, False, True),   # ✅ 都存在且非空，測資存在
    (True, True, True, False, False),   # ❌ user 是空檔，視為不存在
    (True, False, False, False, False), # ❌ product 不存在
    (False, False, False, False, False) # ❌ 都不存在
])
def test_check_if_testdata_exists(monkeypatch, user_exists, user_empty, product_exists, product_empty, expected):
    from workspace.utils.uuid import uuid_checker

    def mock_check_path(path):
        # 只要包含 mock-uuid.json 就視為 mock 的目標
        return "mock-uuid.json" in str(path)

    def mock_file_exists(path):
        if mock_check_path(path):
            if "user" in str(path):
                return user_exists
            elif "product" in str(path):
                return product_exists
        return False

    def mock_is_file_empty(path):
        if mock_check_path(path):
            if "user" in str(path):
                return user_empty
            elif "product" in str(path):
                return product_empty
        return True

    monkeypatch.setattr(uuid_checker, "file_exists", mock_file_exists)
    monkeypatch.setattr(uuid_checker, "is_file_empty", mock_is_file_empty)

    result = uuid_checker.check_if_testdata_exists("mock-uuid")
    assert result == expected

