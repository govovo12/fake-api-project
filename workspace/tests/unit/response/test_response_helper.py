import pytest
from unittest.mock import Mock
from workspace.utils.response.response_helper import (
    get_code_from_dict,
    get_data_field_from_dict,
    get_token_from_dict,
    get_error_message_from_dict,
    get_status_code_from_response,
    get_json_field_from_response,
    get_data_field_from_response,
    get_token_from_response,
    get_error_message_from_response,
)
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.response]

# ✅ 測試 dict 類型 response 工具

def test_get_code_from_dict():
    assert get_code_from_dict({"code": 12345}) == 12345
    assert get_code_from_dict({}) is None

def test_get_data_field_from_dict():
    resp = {"data": {"name": "tony"}}
    assert get_data_field_from_dict(resp, "name") == "tony"
    assert get_data_field_from_dict({}, "name") is None

def test_get_token_from_dict():
    resp = {"data": {"token": "abc123"}}
    assert get_token_from_dict(resp) == "abc123"
    assert get_token_from_dict({}) is None

def test_get_error_message_from_dict():
    assert get_error_message_from_dict({"msg": "失敗"}) == "失敗"
    assert get_error_message_from_dict({"error": "錯誤"}) == "錯誤"
    assert get_error_message_from_dict({}) == "未知錯誤"

# ✅ 測試 requests.Response 類型 response 工具

def test_get_status_code_from_response():
    mock_resp = Mock()
    mock_resp.status_code = 404
    assert get_status_code_from_response(mock_resp) == 404

def test_get_json_field_from_response_success():
    mock_resp = Mock()
    mock_resp.json.return_value = {"id": 1}
    assert get_json_field_from_response(mock_resp, "id") == 1

def test_get_json_field_from_response_failure():
    mock_resp = Mock()
    mock_resp.json.side_effect = Exception("解析失敗")
    assert get_json_field_from_response(mock_resp, "id") is None

def test_get_data_field_from_response_success():
    mock_resp = Mock()
    mock_resp.json.return_value = {"data": {"user": "abc"}}
    assert get_data_field_from_response(mock_resp, "user") == "abc"

def test_get_data_field_from_response_failure():
    mock_resp = Mock()
    mock_resp.json.side_effect = Exception("錯誤")
    assert get_data_field_from_response(mock_resp, "user") is None

def test_get_token_from_response_success():
    mock_resp = Mock()
    mock_resp.json.return_value = {"token": "xyz"}  # ✅ 平鋪結構
    assert get_token_from_response(mock_resp) == "xyz"


def test_get_token_from_response_failure():
    mock_resp = Mock()
    mock_resp.json.side_effect = Exception("錯誤")
    assert get_token_from_response(mock_resp) is None

def test_get_error_message_from_response_success():
    mock_resp = Mock()
    mock_resp.json.return_value = {"msg": "失敗原因"}
    assert get_error_message_from_response(mock_resp) == "失敗原因"

def test_get_error_message_from_response_fallback():
    mock_resp = Mock()
    mock_resp.json.side_effect = Exception("爆了")
    assert get_error_message_from_response(mock_resp) == "回傳格式錯誤"
