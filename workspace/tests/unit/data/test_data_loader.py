import pytest
from pathlib import Path
from unittest.mock import mock_open, patch
from workspace.utils.data.data_loader import load_json
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.data]

def test_load_json_success():
    """
    測試 load_json 函式：成功讀取並解析 JSON 檔案
    """
    mock_data = '{"key": "value"}'
    mock_file = mock_open(read_data=mock_data)
    
    with patch("builtins.open", mock_file):
        result = load_json(Path("fake_path.json"))
    
    assert result == {"key": "value"}  # 檢查是否正確返回字典

def test_load_json_file_not_found():
    """
    測試 load_json 函式：檔案不存在
    """
    result = load_json(Path("fake_path.json"))
    assert result == ResultCode.TOOL_FILE_LOAD_FAILED  # 檢查錯誤碼

def test_load_json_invalid_format():
    """
    測試 load_json 函式：JSON 格式錯誤
    """
    mock_data = '{"key": "value",}'  # 模擬錯誤格式的 JSON
    mock_file = mock_open(read_data=mock_data)
    
    with patch("builtins.open", mock_file):
        result = load_json(Path("fake_path.json"))
    
    assert result == ResultCode.TOOL_FILE_LOAD_FAILED  # 檢查錯誤碼

def test_load_json_permission_error():
    """
    測試 load_json 函式：檔案權限不足
    """
    with patch("builtins.open", side_effect=PermissionError):
        result = load_json(Path("fake_path.json"))
    
    assert result == ResultCode.TOOL_FILE_PERMISSION_DENIED  # 檢查錯誤碼
