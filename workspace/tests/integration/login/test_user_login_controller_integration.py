# -----------------------------
# 📦 測試框架與 mock
# -----------------------------
import pytest
from unittest.mock import patch, Mock

# -----------------------------
# 🧪 被測模組與錯誤碼
# -----------------------------
from workspace.controller.user_login_controller import login_and_report
from workspace.config.rules.error_codes import ResultCode

# -----------------------------
# ✅ 測試標記
# -----------------------------
pytestmark = [pytest.mark.integration, pytest.mark.login, pytest.mark.controller]


@patch("workspace.controller.user_login_controller.login_user", autospec=True)
@patch("workspace.utils.response.response_helper.get_token_from_response", autospec=True)
def test_login_success(mock_token, mock_login_user):
    """✅ 登入成功：login_user 回傳成功 + 有 token"""
    mock_response = Mock(status_code=200)
    mock_token.return_value = "abc123"
    mock_login_user.return_value = (ResultCode.LOGIN_TASK_SUCCESS, "abc123")

    code, token = login_and_report(
        {"username": "user", "password": "pass"},
        {"Content-Type": "application/json"}
    )

    assert code == ResultCode.LOGIN_TASK_SUCCESS
    assert token == "abc123"
    assert mock_login_user.call_count == 1


@patch("workspace.controller.user_login_controller.login_user", autospec=True)
@patch("workspace.utils.response.response_helper.get_token_from_response", autospec=True)
def test_login_failed_401(mock_token, mock_login_user):
    """❌ 登入失敗：帳密錯誤，應不 retry，回傳 LOGIN_API_FAILED"""
    mock_token.return_value = None
    mock_login_user.return_value = (ResultCode.LOGIN_API_FAILED, None)

    code, token = login_and_report(
        {"username": "user", "password": "wrong"},
        {"Content-Type": "application/json"}
    )

    assert code == ResultCode.LOGIN_API_FAILED
    assert token is None
    assert mock_login_user.call_count == 1


@patch("workspace.controller.user_login_controller.login_user", autospec=True)
@patch("workspace.utils.response.response_helper.get_token_from_response", autospec=True)
def test_login_retry_3_times_then_fail(mock_token, mock_login_user):
    """🔁 模擬 3 次連續 Exception，應 retry 滿後回傳 LOGIN_EXCEPTION"""
    mock_token.return_value = None
    mock_login_user.side_effect = [(ResultCode.LOGIN_EXCEPTION, None)] * 3

    code, token = login_and_report(
        {"username": "retry", "password": "fail"},
        {"Content-Type": "application/json"}
    )

    assert code == ResultCode.LOGIN_EXCEPTION
    assert token is None
    assert mock_login_user.call_count == 3
