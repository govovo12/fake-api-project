import pytest
import re
from workspace.modules.fake_data.fake_user.user_generator import generate_user_data

pytestmark = [pytest.mark.unit, pytest.mark.fake_user]


def test_user_data_keys():
    success, user, meta = generate_user_data()
    assert success is True, f"產生失敗: {meta}"
    expected_keys = {"name", "email", "password", "passwordConfirm"}
    assert expected_keys.issubset(user.keys()), f"缺少必要欄位: {expected_keys - user.keys()}"


def test_email_format():
    success, user, meta = generate_user_data()
    assert success is True
    pattern = r"[^@]+@[^@]+\.[^@]+"
    assert re.match(pattern, user["email"]), f"Email 格式錯誤: {user['email']}"


def test_password_confirm_matches():
    success, user, meta = generate_user_data()
    assert success is True
    assert user["password"] == user["passwordConfirm"], "password 與 passwordConfirm 不一致"


def test_password_strength():
    success, user, meta = generate_user_data()
    assert success is True
    assert len(user["password"]) >= 8, "密碼長度不足"


def test_randomness_of_email():
    success1, user1, _ = generate_user_data()
    success2, user2, _ = generate_user_data()
    assert success1 and success2
    assert user1["email"] != user2["email"], "Email 未隨機化，兩次相同"
