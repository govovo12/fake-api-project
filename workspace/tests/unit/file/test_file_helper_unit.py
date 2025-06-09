import pytest
import json
from pathlib import Path
from workspace.utils.file.file_helper import (
    save_json,
    file_exists,
    is_file_empty,
    clear_file,
    generate_testdata_path,
    get_file_name_from_path,
)

# ✅ 測試標記：單元測試 + file 分類
pytestmark = [pytest.mark.unit, pytest.mark.file]


def test_generate_testdata_path_valid_user():
    """
    測試 generate_testdata_path 回傳正確 user 路徑
    """
    path, meta = generate_testdata_path("user", "12345678abcdabcdabcdabcdabcdabcd")
    assert meta is None
    assert path.name == "12345678abcdabcdabcdabcdabcdabcd.json"
    assert "user" in str(path)


def test_generate_testdata_path_invalid_kind():
    """
    測試 generate_testdata_path 傳入錯誤 kind 時應回傳錯誤 meta
    """
    path, meta = generate_testdata_path("banana", "uuid")
    assert path is None
    assert meta["reason"] == "file_helper_invalid_kind"


def test_save_and_check_json(tmp_path):
    """
    測試 save_json 能正確寫入 JSON 檔案並檢查內容存在
    """
    test_path = tmp_path / "test.json"
    success, meta = save_json(test_path, {"name": "test"})
    assert success is True
    assert meta is None
    assert test_path.exists()
    content = json.loads(test_path.read_text(encoding="utf-8"))
    assert content["name"] == "test"


def test_clear_file(tmp_path):
    """
    測試 clear_file 能清空檔案內容
    """
    path = tmp_path / "clear_me.json"
    path.write_text("some data")
    clear_file(path)
    assert path.read_text() == ""


def test_is_file_empty(tmp_path):
    """
    測試 is_file_empty 在空檔與非空檔案的行為
    """
    path = tmp_path / "empty.json"
    path.write_text("")
    assert is_file_empty(path) is True

    path.write_text("abc")
    assert is_file_empty(path) is False


def test_get_file_name_from_path():
    """
    測試 get_file_name_from_path 能正確回傳檔名
    """
    path = Path("/fake/path/data.json")
    assert get_file_name_from_path(path) == "data.json"
