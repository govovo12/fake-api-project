import pytest
from pathlib import Path
from unittest.mock import mock_open
from workspace.utils.file.file_helper import ensure_dir, ensure_file, clear_file
from workspace.config.rules.error_codes import ResultCode

# 標記單元測試及檔案測試
pytestmark = [pytest.mark.unit, pytest.mark.file]

# ===============================
# 測試 ensure_dir 函式
# ===============================

def test_ensure_dir_success(mocker):
    """
    測試 ensure_dir 函式：成功創建目錄
    """
    test_dir = Path("test_dir")
    
    # mock `mkdir` 操作，模擬成功創建目錄
    mock_mkdir = mocker.patch("pathlib.Path.mkdir", return_value=None)
    
    result = ensure_dir(test_dir)
    
    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)  # 確認 mkdir 被正確調用
    assert result == ResultCode.SUCCESS  # 確認返回成功代碼


def test_ensure_dir_failure(mocker):
    """
    測試 ensure_dir 函式：創建目錄失敗
    使用模擬的錯誤
    """
    test_dir = Path("test_dir")
    
    # 模擬 `mkdir` 引發異常
    mock_mkdir = mocker.patch("pathlib.Path.mkdir", side_effect=OSError("Failed to create directory"))
    
    result = ensure_dir(test_dir)
    
    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    assert result == ResultCode.TOOL_DIR_CREATE_FAILED  # 確認返回錯誤代碼


# ===============================
# 測試 ensure_file 函式
# ===============================

def test_ensure_file_success(mocker):
    """
    測試 ensure_file 函式：成功創建檔案
    """
    test_file = Path("test_file.txt")
    
    # mock `touch` 操作，模擬成功創建檔案
    mock_touch = mocker.patch("pathlib.Path.touch", return_value=None)
    
    result = ensure_file(test_file)
    
    mock_touch.assert_called_once()  # 確認 touch 被正確調用
    assert result == ResultCode.SUCCESS  # 確認返回成功代碼


def test_ensure_file_creation_failure(mocker):
    """
    測試 ensure_file 函式：檔案創建失敗
    使用模擬的錯誤
    """
    test_file = Path("test_file.txt")
    
    # 模擬 `touch` 引發異常
    mock_touch = mocker.patch("pathlib.Path.touch", side_effect=OSError("Failed to create file"))
    
    result = ensure_file(test_file)
    
    mock_touch.assert_called_once()
    assert result == ResultCode.TOOL_FILE_CREATE_FAILED  # 確認返回錯誤代碼


# ===============================
# 測試 clear_file 函式
# ===============================

def test_clear_file_success(mocker):
    """
    測試 clear_file 函式：成功清空檔案
    """
    test_file = Path("test_file.txt")
    
    # 模擬檔案存在，並且清空檔案的操作
    mock_exists = mocker.patch("pathlib.Path.exists", return_value=True)  # 模擬檔案存在
    mock_write = mocker.patch("pathlib.Path.write_text", return_value=None)  # 模擬清空檔案
    
    result = clear_file(test_file)
    
    mock_exists.assert_called_once()  # 確保檢查檔案是否存在
    mock_write.assert_called_once_with("", encoding="utf-8")  # 確保清空檔案
    assert result == ResultCode.SUCCESS  # 確認返回成功代碼


def test_clear_file_failure(mocker):
    """
    測試 clear_file 函式：清空檔案失敗
    使用模擬的錯誤
    """
    test_file = Path("test_file.txt")
    
    # 模擬 `write_text` 引發異常
    mock_exists = mocker.patch("pathlib.Path.exists", return_value=True)  # 模擬檔案存在
    mock_write = mocker.patch("pathlib.Path.write_text", side_effect=OSError("Failed to clear file"))  # 模擬清空檔案失敗
    
    result = clear_file(test_file)
    
    mock_exists.assert_called_once()  # 確保檢查檔案是否存在
    mock_write.assert_called_once_with("", encoding="utf-8")  # 確保清空檔案失敗
    assert result == ResultCode.TOOL_FILE_CLEAR_FAILED  # 確認返回錯誤代碼
