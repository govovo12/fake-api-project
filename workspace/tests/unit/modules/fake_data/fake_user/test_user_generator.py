import pytest
from workspace.modules.fake_data.fake_user.user_generator import generate_user_data

pytestmark = [pytest.mark.unit, pytest.mark.fake_user]


def test_generate_user_data_success():
    """
    測試 generate_user_data 成功回傳資料的格式與內容
    """
    success, data, meta = generate_user_data()
    assert success is True
    assert meta is None
    assert isinstance(data, dict)
    assert "name" in data and isinstance(data["name"], str)
    assert "email" in data and isinstance(data["email"], str)
    assert "password" in data and isinstance(data["password"], str)
    assert "passwordConfirm" in data and data["passwordConfirm"] == data["password"]


def test_generate_user_data_handles_exception(monkeypatch):
    """
    模擬 Faker 函式拋出例外，測試錯誤回傳
    """
    def fake_name():
        raise Exception("fake error")

    monkeypatch.setattr(
        "workspace.modules.fake_data.fake_user.user_generator.fake.name",
        fake_name
    )

    success, data, meta = generate_user_data()
    assert success is False
    assert data is None
    assert meta is not None
    assert meta.get("reason") == "user_generator_faker_failed" or meta.get("reason") == "faker_error"
    assert "fake error" in meta.get("message", "")
