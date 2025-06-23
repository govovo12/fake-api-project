# 📦 測試工具
import pytest
from unittest.mock import patch

# 🧪 被測模組
from workspace.controller.user_registration_controller import register_user_with_log

# ⚠️ 錯誤碼常數
from workspace.config.rules.error_codes import ResultCode

# ✅ 測試標記
pytestmark = [pytest.mark.unit, pytest.mark.controller, pytest.mark.register]

# 🧪 測試共用參數
uuid = "abc123"
url = "https://fake.com/users"
headers = {"Content-Type": "application/json"}


@patch("workspace.controller.user_registration_controller.register_user")
@patch("workspace.controller.user_registration_controller.log_simple_result")
def test_register_user_success(mock_log, mock_task):
    """
    測試：底層成功回傳 0，應轉換為 REGISTER_TASK_SUCCESS（10001），並印出
    """
    mock_task.return_value = 0

    result = register_user_with_log(uuid, url, headers)

    mock_log.assert_called_once_with(ResultCode.REGISTER_TASK_SUCCESS)
    assert result == ResultCode.REGISTER_TASK_SUCCESS


@patch("workspace.controller.user_registration_controller.register_user")
@patch("workspace.controller.user_registration_controller.log_simple_result")
def test_register_user_api_fail(mock_log, mock_task):
    """
    測試：底層回傳 FAKER_REGISTER_FAILED（42002），應原樣回傳並印錯誤碼
    """
    mock_task.return_value = ResultCode.FAKER_REGISTER_FAILED

    result = register_user_with_log(uuid, url, headers)

    mock_log.assert_called_once_with(ResultCode.FAKER_REGISTER_FAILED)
    assert result == ResultCode.FAKER_REGISTER_FAILED


@patch("workspace.controller.user_registration_controller.register_user")
@patch("workspace.controller.user_registration_controller.log_simple_result")
def test_register_user_exception(mock_log, mock_task):
    """
    測試：底層回傳 FAKER_REGISTER_EXCEPTION（42003），應原樣回傳並印錯誤碼
    """
    mock_task.return_value = ResultCode.FAKER_REGISTER_EXCEPTION

    result = register_user_with_log(uuid, url, headers)

    mock_log.assert_called_once_with(ResultCode.FAKER_REGISTER_EXCEPTION)
    assert result == ResultCode.FAKER_REGISTER_EXCEPTION


@patch("workspace.controller.user_registration_controller.register_user")
@patch("workspace.controller.user_registration_controller.log_simple_result")
def test_register_user_load_fail(mock_log, mock_task):
    """
    測試：底層回傳 TOOL_FILE_LOAD_FAILED（40001），應原樣回傳並印錯誤碼
    """
    mock_task.return_value = ResultCode.TOOL_FILE_LOAD_FAILED

    result = register_user_with_log(uuid, url, headers)

    mock_log.assert_called_once_with(ResultCode.TOOL_FILE_LOAD_FAILED)
    assert result == ResultCode.TOOL_FILE_LOAD_FAILED
