import pytest
from unittest.mock import patch, Mock
from workspace.modules.login.login_user import login_user
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.login]


def test_login_success():
    """✅ 測試登入成功，應取得 token 並回傳成功碼"""
    cred = {"username": "user", "password": "pass"}
    headers = {"Content-Type": "application/json"}
    mock_response = Mock(status_code=200)
    mock_response.json.return_value = {"token": "abc123"}

    with patch("workspace.modules.login.login_user.post", return_value=mock_response):
        with patch("workspace.modules.login.login_user.get_token_from_response", return_value="abc123"):
            code, token = login_user(cred, headers)

    assert code == ResultCode.LOGIN_TASK_SUCCESS
    assert token == "abc123"


def test_login_failed_invalid_credentials():
    """❌ 測試帳密錯誤，應回傳失敗碼與無 token"""
    cred = {"username": "user", "password": "wrong"}
    headers = {"Content-Type": "application/json"}
    mock_response = Mock(status_code=401)
    mock_response.json.return_value = {"msg": "Unauthorized"}

    with patch("workspace.modules.login.login_user.post", return_value=mock_response):
        code, token = login_user(cred, headers)

    assert code == ResultCode.LOGIN_API_FAILED
    assert token is None


def test_login_with_missing_fields():
    """⚠️ 測試缺欄位（只有 username）"""
    cred = {"username": "user"}  # 沒有 password
    headers = {"Content-Type": "application/json"}
    mock_response = Mock(status_code=400)
    mock_response.json.return_value = {"error": "missing password"}

    with patch("workspace.modules.login.login_user.post", return_value=mock_response):
        code, token = login_user(cred, headers)

    assert code == ResultCode.LOGIN_API_FAILED
    assert token is None


def test_login_request_exception():
    """💥 模擬 requests 發生例外（如 timeout）"""
    cred = {"username": "user", "password": "pass"}
    headers = {"Content-Type": "application/json"}

    with patch("workspace.modules.login.login_user.post", side_effect=Exception("Timeout")):
        code, token = login_user(cred, headers)

    assert code == ResultCode.LOGIN_EXCEPTION
    assert token is None
