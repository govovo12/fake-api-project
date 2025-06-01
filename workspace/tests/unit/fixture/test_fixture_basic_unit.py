import pytest
from requests import Session
from datetime import datetime

pytestmark = [pytest.mark.unit, pytest.mark.fixture]

def test_fake_status_code_value(fake_status_code):
    """fake_status_code fixture 應回傳 200"""
    assert fake_status_code == 200

def test_fake_user_data(fake_user_data):
    """fake_user_data fixture 回傳假 user dict"""
    user = fake_user_data
    assert isinstance(user, dict)
    assert "name" in user and "email" in user

def test_temp_file_content(temp_file):
    """temp_file fixture 應產生固定內容檔案"""
    content = temp_file.read_text(encoding="utf-8")
    assert content == "stub file content"

def test_fake_logger_calls(fake_logger):
    """fake_logger fixture 能記錄 info/warn/error"""
    fake_logger.info("abc")
    fake_logger.warn("def")
    fake_logger.error("ghi")
    assert fake_logger.messages == [
        ("info", "abc"),
        ("warn", "def"),
        ("error", "ghi"),
    ]

def test_fake_session_type(fake_session):
    """fake_session fixture 為 requests.Session 類型"""
    assert isinstance(fake_session, Session)

def test_stub_cart_payload_keys(stub_cart_payload):
    """stub_cart_payload 應含 userId、date、products"""
    cart = stub_cart_payload
    assert "userId" in cart
    assert "date" in cart
    assert "products" in cart

def test_fake_now_value(fake_now):
    """fake_now fixture 產生固定 datetime"""
    assert isinstance(fake_now, datetime)
    assert fake_now.year == 2024 and fake_now.month == 6

def test_temp_env_fixture(temp_env_fixture):
    """temp_env_fixture 執行後應存在 TEST_ENV"""
    import os
    assert os.environ.get("TEST_ENV") == "1"
