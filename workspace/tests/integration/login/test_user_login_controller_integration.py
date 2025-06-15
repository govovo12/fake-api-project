import pytest
from unittest.mock import patch, Mock
from workspace.controller.user_login_controller import login_and_report
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.integration, pytest.mark.login]


@patch("workspace.modules.login.login_user.post")
@patch("workspace.modules.login.login_user.get_token_from_response")
def test_login_controller_success(mock_token, mock_post):
    """
    ✅ 模擬登入成功：post 回傳 200 且 token 存在
    """
    mock_response = Mock(status_code=200)
    mock_post.return_value = mock_response
    mock_token.return_value = "abc123"

    code, token = login_and_report(
        cred={"username": "johnd", "password": "m38rmF$"},
        headers={"Content-Type": "application/json"}
    )

    assert code == ResultCode.LOGIN_TASK_SUCCESS
    assert token == "abc123"


@patch("workspace.modules.login.login_user.post")
@patch("workspace.modules.login.login_user.get_token_from_response")
def test_login_controller_api_failed(mock_token, mock_post):
    """
    ❌ 模擬帳密錯誤（回傳 401）：應直接回傳失敗，不 retry
    """
    mock_response = Mock(status_code=401)
    mock_post.return_value = mock_response
    mock_token.return_value = None

    code, token = login_and_report(
        cred={"username": "johnd", "password": "wrong_password"},
        headers={"Content-Type": "application/json"}
    )

    assert code == ResultCode.LOGIN_API_FAILED
    assert token is None


@patch("workspace.modules.login.login_user.post")
@patch("workspace.modules.login.login_user.get_token_from_response")
def test_login_controller_retry_then_fail(mock_token, mock_post):
    """
    🔁 模擬發生三次例外（如 timeout），應 retry 三次後返回例外錯誤碼
    """
    mock_post.side_effect = Exception("timeout")
    mock_token.return_value = None

    code, token = login_and_report(
        cred={"username": "johnd", "password": "timeout"},
        headers={"Content-Type": "application/json"}
    )

    assert code == ResultCode.LOGIN_EXCEPTION
    assert token is None
