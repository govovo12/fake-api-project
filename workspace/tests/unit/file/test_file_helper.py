import pytest
from pathlib import Path
import tempfile
from unittest.mock import PropertyMock

from workspace.utils.mock.mock_helper import mock_function

pytestmark = [pytest.mark.unit, pytest.mark.file]

from workspace.config.rules.error_codes import ResultCode
from workspace.utils.file.file_helper import (
    ensure_dir,
    ensure_file,
    file_exists,
    is_file_empty,
    clear_file,
    delete_file
)


def test_ensure_dir_success(tmp_path):
    """✅ 建立新目錄成功"""
    test_path = tmp_path / "subdir"
    result = ensure_dir(test_path)
    assert result == ResultCode.SUCCESS
    assert test_path.exists()


def test_ensure_dir_invalid_type():
    """💥 傳入非 Path 類型回錯誤碼"""
    result = ensure_dir("not_a_path")
    assert result == ResultCode.TOOL_INVALID_FILE_DATA


def test_ensure_dir_exception(monkeypatch):
    """💥 模擬目錄建立失敗"""
    monkeypatch.setattr(Path, "mkdir", mock_function(side_effect=OSError("mkdir fail")))
    result = ensure_dir(Path("gome/fake/dir"))
    assert result == ResultCode.TOOL_DIR_CREATE_FAILED


def test_ensure_file_success(tmp_path):
    """✅ 建立新空檔案成功"""
    test_path = tmp_path / "test.txt"
    result = ensure_file(test_path)
    assert result == ResultCode.SUCCESS
    assert test_path.exists()


def test_ensure_file_already_exists(tmp_path):
    """⏳ 檔案已存在，直接回成功"""
    file_path = tmp_path / "temp.txt"
    file_path.write_text("hello")
    result = ensure_file(file_path)
    assert result == ResultCode.SUCCESS


def test_ensure_file_invalid_type():
    """💥 傳入非 Path 類型，回錯誤碼"""
    result = ensure_file(123)
    assert result == ResultCode.TOOL_INVALID_FILE_DATA


def test_ensure_file_exception(monkeypatch, tmp_path):
    """💥 模擬檔案建立失敗"""
    monkeypatch.setattr(Path, "touch", mock_function(side_effect=OSError("touch fail")))
    result = ensure_file(tmp_path / "fake_file.txt")
    assert result == ResultCode.TOOL_FILE_CREATE_FAILED



def test_file_exists_true_and_false(tmp_path):
    """✅ 正反測試：檔案存在與不存在"""
    temp_file = tmp_path / "tempfile.txt"
    temp_file.write_text("data")
    assert file_exists(temp_file) is True
    temp_file.unlink()
    assert file_exists(temp_file) is False


def test_file_exists_invalid_type():
    """💥 傳入非 Path，應回 False"""
    assert file_exists("bad input") is False


def test_is_file_empty_true_and_false(tmp_path):
    """✅ 檔案為空與非空的正反測試"""
    path = tmp_path / "emptyfile.txt"
    path.write_text("")
    assert is_file_empty(path) is True
    path.write_text("data")
    assert is_file_empty(path) is False


def test_is_file_empty_invalid_type():
    """💥 傳入非 Path，回錯誤碼"""
    result = is_file_empty("abc")
    assert result == ResultCode.TOOL_INVALID_FILE_DATA


def test_is_file_empty_stat_oserror(monkeypatch):
    """💥 模擬 stat() 呼叫失敗，觸發錯誤碼"""
    monkeypatch.setattr(Path, "stat", mock_function(side_effect=OSError("stat fail")))
    result = is_file_empty(Path("bad/path.txt"))
    assert result == ResultCode.TOOL_FILE_STAT_FAILED


class BrokenStat:
    @property
    def st_size(self):
        raise OSError("fail on access")


def test_is_file_empty_st_size_oserror(monkeypatch):
    """💥 模擬 stat().st_size 屬性存取失敗，觸發錯誤碼"""
    broken_stat = BrokenStat()
    monkeypatch.setattr(type(broken_stat), 'st_size', PropertyMock(side_effect=OSError("fail on access")))
    monkeypatch.setattr(Path, "stat", mock_function(return_value=broken_stat))
    result = is_file_empty(Path("fake/file.txt"))
    assert result == ResultCode.TOOL_FILE_STAT_FAILED


def test_clear_file_success(tmp_path):
    """✅ 清空檔案成功"""
    path = tmp_path / "file_to_clear.txt"
    path.write_text("123")
    result = clear_file(path)
    assert result == ResultCode.SUCCESS
    assert path.read_text() == ""


def test_clear_file_invalid_type():
    """💥 傳入非 Path 回錯誤碼"""
    result = clear_file(None)
    assert result == ResultCode.TOOL_INVALID_FILE_DATA


def test_delete_file_success_and_not_exist(tmp_path):
    """⏳ 刪除存在與不存在的檔案均回成功"""
    path = tmp_path / "file_to_delete.txt"
    path.write_text("delete me")
    assert path.exists()
    result1 = delete_file(path)
    assert result1 == ResultCode.SUCCESS
    result2 = delete_file(path)
    assert result2 == ResultCode.SUCCESS


def test_delete_file_invalid_type():
    """💥 傳入非 Path 回錯誤碼"""
    result = delete_file("bad-path")
    assert result == ResultCode.TOOL_INVALID_FILE_DATA


def test_delete_file_exception(monkeypatch):
    """💥 模擬 unlink 失敗，回錯誤碼"""
    monkeypatch.setattr(Path, "exists", mock_function(return_value=True))
    monkeypatch.setattr(Path, "unlink", mock_function(side_effect=OSError("unlink fail")))
    result = delete_file(Path("non/deletable/file.txt"))
    assert result == ResultCode.TOOL_FILE_DELETE_FAILED
