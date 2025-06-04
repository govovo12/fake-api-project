# workspace/tests/unit/modules/fake_data/fake_user/test_user_generator.py

import pytest
import re
from workspace.modules.fake_data.fake_user.user_generator import generate_fake_user_data

pytestmark = [pytest.mark.unit, pytest.mark.fake_user]

def test_user_data_keys():
    """
    確認產生的 user data 包含所有必要欄位
    """
    user = generate_fake_user_data()
    expected_keys = {"name", "email", "password", "passwordConfirm"}
    assert expected_keys.issubset(user.keys()), f"缺少必要欄位: {expected_keys - user.keys()}"

def test_email_format():
    """
    驗證 email 格式符合標準格式
    """
    user = generate_fake_user_data()
    email = user["email"]
    pattern = r"[^@]+@[^@]+\.[^@]+"
    assert re.match(pattern, email), f"Email 格式錯誤: {email}"

def test_password_confirm_matches():
    """
    確認 password 與 passwordConfirm 欄位一致
    """
    user = generate_fake_user_data()
    assert user["password"] == user["passwordConfirm"], "password 與 passwordConfirm 不一致"

def test_password_strength():
    """
    驗證密碼長度至少為 8（符合基本安全需求）
    """
    user = generate_fake_user_data()
    assert len(user["password"]) >= 8, "密碼長度不足"

def test_randomness_of_email():
    """
    測試 email 每次產生皆不同（簡單兩次比較）
    """
    user1 = generate_fake_user_data()
    user2 = generate_fake_user_data()
    assert user1["email"] != user2["email"], "Email 未隨機化，兩次相同"
