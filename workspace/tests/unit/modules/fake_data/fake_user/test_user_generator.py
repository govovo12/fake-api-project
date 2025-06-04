# workspace/tests/unit/modules/fake_data/fake_user/test_user_generator.py

import pytest
import re
from workspace.modules.fake_data.fake_user.user_generator import generate_fake_user_data
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.fake_user]

def test_user_data_keys():
    """
    確認產生的 user data 包含所有必要欄位
    """
    code, user = generate_fake_user_data()
    assert code == ResultCode.SUCCESS, f"產生失敗，錯誤碼: {code}"
    expected_keys = {"name", "email", "password", "passwordConfirm"}
    assert expected_keys.issubset(user.keys()), f"缺少必要欄位: {expected_keys - user.keys()}"

def test_email_format():
    """
    驗證 email 格式符合標準格式
    """
    code, user = generate_fake_user_data()
    assert code == ResultCode.SUCCESS
    pattern = r"[^@]+@[^@]+\.[^@]+"
    assert re.match(pattern, user["email"]), f"Email 格式錯誤: {user['email']}"

def test_password_confirm_matches():
    """
    確認 password 與 passwordConfirm 欄位一致
    """
    code, user = generate_fake_user_data()
    assert code == ResultCode.SUCCESS
    assert user["password"] == user["passwordConfirm"], "password 與 passwordConfirm 不一致"

def test_password_strength():
    """
    驗證密碼長度至少為 8（符合基本安全需求）
    """
    code, user = generate_fake_user_data()
    assert code == ResultCode.SUCCESS
    assert len(user["password"]) >= 8, "密碼長度不足"

def test_randomness_of_email():
    """
    測試 email 每次產生皆不同（簡單兩次比較）
    """
    code1, user1 = generate_fake_user_data()
    code2, user2 = generate_fake_user_data()
    assert code1 == ResultCode.SUCCESS and code2 == ResultCode.SUCCESS
    assert user1["email"] != user2["email"], "Email 未隨機化，兩次相同"
