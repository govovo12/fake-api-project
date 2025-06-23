# 📦 測試工具
import pytest
from unittest.mock import Mock

# 🧪 被測模組
from workspace.controller.user_registration_controller import register_user_with_log

# ⚠️ 錯誤碼常數
from workspace.config.rules.error_codes import ResultCode

# ✅ 測試標記：整合 + 控制器 + 註冊任務
pytestmark = [pytest.mark.integration, pytest.mark.controller, pytest.mark.register]


def test_register_user_success(monkeypatch):
    """
    整合測試：模擬工具模組成功，應回傳 REGISTER_TASK_SUCCESS
    """
    monkeypatch.setattr(
        "workspace.modules.register.register_user.load_json",
        lambda path: {
            "email": "a@a.com",
            "username": "test_user",
            "password": "1234",
            "name": {"firstname": "John", "lastname": "Doe"},
            "address": {"city": "X", "street": "Y", "zipcode": "123", "number": 1},
            "phone": "0000000"
        }
    )
    monkeypatch.setattr(
        "workspace.modules.register.register_user.post",
        lambda **kwargs: Mock(status_code=201)
    )
    monkeypatch.setattr(
        "workspace.modules.register.register_user.get_status_code_from_response",
        lambda resp: resp.status_code
    )

    result = register_user_with_log("fake_uuid", "https://fake.url", {"Content-Type": "application/json"})
    assert result == ResultCode.REGISTER_TASK_SUCCESS


def test_register_user_api_failed(monkeypatch):
    """
    整合測試：模擬 API 回 400，應回傳 FAKER_REGISTER_FAILED
    """
    monkeypatch.setattr(
        "workspace.modules.register.register_user.load_json",
        lambda path: {
            "email": "a@a.com", "username": "test", "password": "1234",
            "name": {"firstname": "f", "lastname": "l"},
            "address": {"city": "X", "street": "Y", "zipcode": "123", "number": 1},
            "phone": "0000000"
        }
    )
    monkeypatch.setattr(
        "workspace.modules.register.register_user.post",
        lambda **kwargs: Mock(status_code=400)
    )
    monkeypatch.setattr(
        "workspace.modules.register.register_user.get_status_code_from_response",
        lambda resp: resp.status_code
    )

    result = register_user_with_log("fake_uuid", "https://fake.url", {"Content-Type": "application/json"})
    assert result == ResultCode.FAKER_REGISTER_FAILED


def test_register_user_exception(monkeypatch):
    """
    整合測試：模擬 post 發生例外，應回傳 FAKER_REGISTER_EXCEPTION
    """
    monkeypatch.setattr(
        "workspace.modules.register.register_user.load_json",
        lambda path: {
            "email": "a@a.com", "username": "test", "password": "1234",
            "name": {"firstname": "f", "lastname": "l"},
            "address": {"city": "X", "street": "Y", "zipcode": "123", "number": 1},
            "phone": "0000000"
        }
    )

    def raise_error(**kwargs):
        raise Exception("mocked post timeout")

    monkeypatch.setattr("workspace.modules.register.register_user.post", raise_error)

    result = register_user_with_log("fake_uuid", "https://fake.url", {"Content-Type": "application/json"})
    assert result == ResultCode.FAKER_REGISTER_EXCEPTION
