# workspace/tests/unit/modules/register/test_build_register_payload.py

import pytest
from unittest.mock import patch
from workspace.modules.register import build_register_payload
from workspace.config.rules import error_codes
from workspace.utils.asserts.assert_helper import assert_in_keys

# 📌 標記這是 register 類別模組的單元測試
pytestmark = [pytest.mark.unit, pytest.mark.register]

# ✅ 測試情境 1：正常組裝成功
@patch("workspace.modules.register.build_register_payload.env_manager.EnvManager.load_env_dict")
@patch("workspace.modules.register.build_register_payload.data_loader.load_json")
def test_build_payload_success(mock_load_json, mock_load_env):
    mock_load_json.return_value = {
        "name": "Tony Chen",
        "email": "tony@mail.com",
        "password": "abc123"
    }
    mock_load_env.return_value = {
        "REGISTER_FIELDS": "username,password,email,name"
    }

    code, payload = build_register_payload.build_register_payload("fake.json")
    assert code == error_codes.ResultCode.SUCCESS
    assert_in_keys(payload, ["username", "password", "email", "name"])
    assert_in_keys(payload["name"], ["firstname", "lastname"])
    assert payload["username"] == "tony"
    assert payload["name"]["firstname"] == "Tony"
    assert payload["name"]["lastname"] == "Chen"

# ✅ 測試情境 2：user 檔案讀取失敗
@patch("workspace.modules.register.build_register_payload.env_manager.EnvManager.load_env_dict")
@patch("workspace.modules.register.build_register_payload.data_loader.load_json", side_effect=Exception("file not found"))
def test_build_payload_json_fail(mock_load_json, mock_load_env):
    mock_load_env.return_value = {
        "REGISTER_FIELDS": "username,password,email,name"
    }

    code, result = build_register_payload.build_register_payload("notfound.json")
    assert code == error_codes.ResultCode.USER_TESTDATA_NOT_FOUND
    assert "msg" in result

# ✅ 測試情境 3：user 測資缺少欄位，導致 KeyError
@patch("workspace.modules.register.build_register_payload.env_manager.EnvManager.load_env_dict")
@patch("workspace.modules.register.build_register_payload.data_loader.load_json")
def test_build_payload_missing_key(mock_load_json, mock_load_env):
    mock_load_json.return_value = {
        "email": "abc@mail.com",
        "password": "abc123"
        # 故意不給 name
    }
    mock_load_env.return_value = {
        "REGISTER_FIELDS": "username,password,email,name"
    }

    code, result = build_register_payload.build_register_payload("fake.json")
    assert code == error_codes.ResultCode.PAYLOAD_BUILD_FAIL
    assert "msg" in result

# ✅ 測試情境 4：name 欄位只有一個字（無法分出 lastname）
@patch("workspace.modules.register.build_register_payload.env_manager.EnvManager.load_env_dict")
@patch("workspace.modules.register.build_register_payload.data_loader.load_json")
def test_build_payload_single_name(mock_load_json, mock_load_env):
    mock_load_json.return_value = {
        "name": "Tony",
        "email": "tony@mail.com",
        "password": "abc123"
    }
    mock_load_env.return_value = {
        "REGISTER_FIELDS": "username,password,email,name"
    }

    code, payload = build_register_payload.build_register_payload("oneword.json")
    assert code == error_codes.ResultCode.SUCCESS
    assert payload["name"]["firstname"] == "Tony"
    assert payload["name"]["lastname"] == "Tony"  # fallback 為單字重複

# ✅ 測試情境 5：env 中沒有 REGISTER_FIELDS（使用預設）
@patch("workspace.modules.register.build_register_payload.env_manager.EnvManager.load_env_dict")
@patch("workspace.modules.register.build_register_payload.data_loader.load_json")
def test_build_payload_env_missing_fields(mock_load_json, mock_load_env):
    mock_load_json.return_value = {
        "name": "Alice Wonderland",
        "email": "alice@mail.com",
        "password": "xyz123"
    }
    mock_load_env.return_value = {}  # 故意缺少 REGISTER_FIELDS

    code, payload = build_register_payload.build_register_payload("default.json")
    assert code == error_codes.ResultCode.SUCCESS
    assert_in_keys(payload, ["username", "password", "email", "name"])
    assert payload["username"] == "alice"
