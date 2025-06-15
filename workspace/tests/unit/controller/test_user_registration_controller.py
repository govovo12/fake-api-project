import pytest
from unittest.mock import patch
from workspace.controller.user_registration_controller import register_user_with_log
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.controller, pytest.mark.register]

uuid = "abc123"
url = "https://fake.com/users"
headers = {"Content-Type": "application/json"}


@patch("workspace.controller.user_registration_controller.register_user")
@patch("workspace.controller.user_registration_controller.log_simple_result")
def test_register_user_success(mock_log, mock_task):
    """
    測試任務模組成功回傳 0 → 子控制器應回傳 REGISTER_TASK_SUCCESS（10001）
    """
    mock_task.return_value = 0

    result = register_user_with_log(uuid, url, headers)

    mock_log.assert_called_once_with(0)
    assert result == ResultCode.REGISTER_TASK_SUCCESS


@patch("workspace.controller.user_registration_controller.register_user")
@patch("workspace.controller.user_registration_controller.log_simple_result")
def test_register_user_api_fail(mock_log, mock_task):
    """
    測試任務模組回傳註冊失敗錯誤碼（42002）
    """
    mock_task.return_value = ResultCode.FAKER_REGISTER_FAILED

    result = register_user_with_log(uuid, url, headers)

    mock_log.assert_called_once_with(ResultCode.FAKER_REGISTER_FAILED)
    assert result == ResultCode.FAKER_REGISTER_FAILED


@patch("workspace.controller.user_registration_controller.register_user")
@patch("workspace.controller.user_registration_controller.log_simple_result")
def test_register_user_exception(mock_log, mock_task):
    """
    測試任務模組回傳 exception 錯誤碼（42003）
    """
    mock_task.return_value = ResultCode.FAKER_REGISTER_EXCEPTION

    result = register_user_with_log(uuid, url, headers)

    mock_log.assert_called_once_with(ResultCode.FAKER_REGISTER_EXCEPTION)
    assert result == ResultCode.FAKER_REGISTER_EXCEPTION


@patch("workspace.controller.user_registration_controller.register_user")
@patch("workspace.controller.user_registration_controller.log_simple_result")
def test_register_user_load_fail(mock_log, mock_task):
    """
    測試任務模組回傳測資載入錯誤碼（40001）
    """
    mock_task.return_value = ResultCode.TOOL_FILE_LOAD_FAILED

    result = register_user_with_log(uuid, url, headers)

    mock_log.assert_called_once_with(ResultCode.TOOL_FILE_LOAD_FAILED)
    assert result == ResultCode.TOOL_FILE_LOAD_FAILED
