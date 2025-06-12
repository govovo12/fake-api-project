import pytest
from modules.fake_data.fake_user.user_generator import generate_user_data
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.fake_user]

def test_generate_user_data_success():
    """
    成功產生用戶資料，應回傳 dict 且欄位符合規則
    """
    result = generate_user_data()
    assert result != ResultCode.FAKER_GENERATE_FAILED
    assert isinstance(result, dict)
    assert "username" in result
    assert "email" in result
    assert "password" in result
    assert 3 <= len(result["username"]) <= 50
    assert len(result["email"]) <= 100
    assert 8 <= len(result["password"]) <= 16

def test_generate_user_data_invalid_username():
    """
    模擬錯誤 username（過短），應回傳 FAKER_GENERATE_FAILED
    """
    result = generate_user_data(username="Yo")
    assert result == ResultCode.FAKER_GENERATE_FAILED

def test_generate_user_data_invalid_email():
    """
    模擬錯誤 email（格式錯誤），應回傳 FAKER_GENERATE_FAILED
    """
    result = generate_user_data(email="invalid-email.com")
    assert result == ResultCode.FAKER_GENERATE_FAILED

def test_generate_user_data_invalid_password():
    """
    模擬錯誤 password（過短），應回傳 FAKER_GENERATE_FAILED
    """
    result = generate_user_data(password="123")
    assert result == ResultCode.FAKER_GENERATE_FAILED
