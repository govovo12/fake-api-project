import pytest
from unittest.mock import patch, Mock
from workspace.modules.register.register_user import register_user
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.register]

uuid = "abc123"
url = "https://fake.com/users"
headers = {"Content-Type": "application/json"}


@patch("workspace.modules.register.register_user.load_json")
@patch("workspace.modules.register.register_user.post")
@patch("workspace.modules.register.register_user.get_status_code_from_response")
def test_register_user_success(mock_status, mock_post, mock_load):
    """
    測試成功註冊，應回傳 0
    """
    mock_load.return_value = {"username": "user", "email": "x@x.com", "password": "test1234"}
    mock_status.return_value = 201

    result = register_user(uuid, url, headers)
    assert result == 0


@patch("workspace.modules.register.register_user.load_json")
@patch("workspace.modules.register.register_user.post")
@patch("workspace.modules.register.register_user.get_status_code_from_response")
def test_register_user_api_failed(mock_status, mock_post, mock_load):
    """
    測試 API 回傳非成功狀態碼，應回傳 FAKER_REGISTER_FAILED
    """
    mock_load.return_value = {"username": "user", "email": "x@x.com", "password": "test1234"}
    mock_status.return_value = 400

    result = register_user(uuid, url, headers)
    assert result == ResultCode.FAKER_REGISTER_FAILED


@patch("workspace.modules.register.register_user.load_json")
@patch("workspace.modules.register.register_user.post", side_effect=Exception("timeout"))
def test_register_user_exception(mock_post, mock_load):
    """
    測試發生 requests 例外時，應回傳 FAKER_REGISTER_EXCEPTION
    """
    mock_load.return_value = {"username": "user", "email": "x@x.com", "password": "test1234"}

    result = register_user(uuid, url, headers)
    assert result == ResultCode.FAKER_REGISTER_EXCEPTION


@patch("workspace.modules.register.register_user.load_json")
def test_register_user_load_failed(mock_load):
    """
    測試載入測資失敗（load_json 回傳錯誤碼）
    """
    mock_load.return_value = ResultCode.TOOL_FILE_LOAD_FAILED

    result = register_user(uuid, url, headers)
    assert result == ResultCode.TOOL_FILE_LOAD_FAILED
