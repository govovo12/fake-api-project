import pytest
from unittest.mock import patch
from pathlib import Path
from workspace.utils.data.data_initializer import write_empty_data_file
from workspace.config.rules.error_codes import ResultCode

# 標記單元測試
pytestmark = [pytest.mark.unit, pytest.mark.data]

def test_write_empty_data_file_success():
    """
    測試 write_empty_data_file 函式：
    當 save_json 成功時應回傳 ResultCode.SUCCESS
    """
    path = Path("test_output.json")
    data = {"id": "", "name": "test"}

    # 正確 patch 路徑：patch data_initializer 作用域中的 save_json
    with patch("workspace.utils.data.data_initializer.save_json", return_value=ResultCode.SUCCESS) as mock_save:
        result = write_empty_data_file(path, data)

        # 驗證回傳正確
        assert result == ResultCode.SUCCESS

        # 驗證 save_json 確實被呼叫
        mock_save.assert_called_once_with(path, data)


def test_write_empty_data_file_failure():
    """
    測試 write_empty_data_file 函式：
    當 save_json 發生錯誤（例如寫入失敗）時應回傳 TOOL_USER_TESTDATA_FILE_WRITE_FAILED
    """
    path = Path("test_output.json")
    data = {"id": "", "name": "test"}

    # 模擬儲存資料時出現錯誤，並返回自定義錯誤碼
    with patch("workspace.utils.data.data_initializer.save_json", side_effect=Exception("Write failed")):
        result = write_empty_data_file(path, data)

        # 檢查返回的錯誤碼是否為 TOOL_USER_TESTDATA_FILE_WRITE_FAILED
        assert result == ResultCode.TOOL_USER_TESTDATA_FILE_WRITE_FAILED
