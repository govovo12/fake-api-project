import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
from workspace.utils.data.data_loader import load_json,save_json
from workspace.config.rules.error_codes import ResultCode

# 標記單元測試
pytestmark = [pytest.mark.unit, pytest.mark.data]

def test_load_json_permission_error(tmpdir):
    """
    測試 load_json 函式：檔案權限不足
    """
    # 使用 pytest 提供的 tmpdir 創建臨時檔案
    temp_file_path = tmpdir.join("protected_file.json")
    
    # 寫入一些測試資料
    temp_file_path.write('{"key": "value"}')

    # 給檔案設置為只讀，模擬權限不足的情況
    temp_file_path.chmod(0o444)  # 只讀權限

    # 模擬檔案權限錯誤
    with patch("builtins.open", side_effect=PermissionError):
        result = load_json(temp_file_path)

    # Debug 輸出，確認是否捕捉到 PermissionError
    print("測試返回的錯誤碼：", result)
    
    # 檢查返回的錯誤碼是否為權限錯誤
    assert result == ResultCode.TOOL_FILE_PERMISSION_DENIED  # 使用 40017 作為期望錯誤碼

def test_load_json_file_not_found():
    """
    測試 load_json 函式：檔案不存在
    """
    path = Path("non_existent_file.json")
    
    # 模擬檔案不存在的情況
    result = load_json(path)
    
    # 檢查返回的錯誤碼是否為檔案不存在錯誤
    assert result == ResultCode.TOOL_FILE_LOAD_FAILED

def test_load_json_invalid_json():
    """
    測試 load_json 函式：JSON 格式錯誤
    """
    path = Path("invalid_json.json")
    
    # 模擬讀取 JSON 解析錯誤
    with patch("builtins.open", mock_open(read_data="invalid json")):
        result = load_json(path)
    
    # 檢查返回的錯誤碼是否為 JSON 解析錯誤
    assert result == ResultCode.TOOL_FILE_LOAD_FAILED

def test_save_json_success():
    """
    測試 save_json 函式：儲存成功
    """
    path = Path("output.json")
    data = {"key": "value"}
    
    # 模擬成功儲存 JSON
    with patch("builtins.open", mock_open()) as mock_file:
        result = save_json(path, data)
        
        # 檢查返回的結果是否為成功代碼
        assert result == ResultCode.SUCCESS
        mock_file.assert_called_once_with(path, "w", encoding="utf-8")

def test_save_json_failure():
    """
    測試 save_json 函式：儲存失敗
    """
    path = Path("output.json")
    data = {"key": "value"}
    
    # 模擬寫入檔案失敗
    with patch("builtins.open", side_effect=Exception("Write failed")):
        result = save_json(path, data)
    
    # 檢查返回的錯誤碼是否為儲存失敗錯誤
    assert result == ResultCode.TOOL_FILE_WRITE_FAILED

def test_extract_fields_from_dict_success():
    """
    測試 extract_fields_from_dict：正確擷取指定欄位
    """
    from workspace.utils.data.data_loader import extract_fields_from_dict

    data = {
        "username": "user123",
        "password": "pass456",
        "email": "x@x.com"
    }
    result = extract_fields_from_dict(data, ["username", "password"])
    assert result == {"username": "user123", "password": "pass456"}


def test_extract_fields_from_dict_missing_keys():
    """
    測試 extract_fields_from_dict：指定欄位部分不存在
    """
    from workspace.utils.data.data_loader import extract_fields_from_dict

    data = {"username": "user123"}
    result = extract_fields_from_dict(data, ["username", "password"])
    assert result == {"username": "user123"}


def test_extract_fields_from_dict_not_dict():
    """
    測試 extract_fields_from_dict：輸入非 dict
    """
    from workspace.utils.data.data_loader import extract_fields_from_dict

    data = "not a dict"
    result = extract_fields_from_dict(data, ["username"])
    assert result == {}
