import pytest
import requests
from unittest.mock import MagicMock
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

pytestmark = [pytest.mark.unit, pytest.mark.response]

# === dict 類型 response ===

def test_get_code_from_dict_exists():
    resp = {"code": 200}
    assert get_code_from_dict(resp) == 200

def test_get_code_from_dict_missing():
    resp = {"msg": "no code"}
    assert get_code_from_dict(resp) is None

def test_get_data_field_from_dict_found():
    resp = {"data": {"uid": 123}}
    assert get_data_field_from_dict(resp, "uid") == 123

def test_get_data_field_from_dict_not_found():
    resp = {"data": {}}
    assert get_data_field_from_dict(resp, "uid") is None

def test_get_token_from_dict_found():
    resp = {"data": {"token": "abc123"}}
    assert get_token_from_dict(resp) == "abc123"

def test_get_token_from_dict_missing():
    resp = {"data": {}}
    assert get_token_from_dict(resp) is None

def test_get_error_message_from_dict_msg():
    resp = {"msg": "錯誤訊息"}
    assert get_error_message_from_dict(resp) == "錯誤訊息"

def test_get_error_message_from_dict_error():
    resp = {"error": "失敗原因"}
    assert get_error_message_from_dict(resp) == "失敗原因"

def test_get_error_message_from_dict_fallback():
    resp = {}
    assert get_error_message_from_dict(resp) == "未知錯誤"

# === requests.Response 類型 response ===

def test_get_status_code_from_response():
    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.status_code = 200
    assert get_status_code_from_response(mock_resp) == 200

def test_get_json_field_from_response_success():
    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.json.return_value = {"token": "abc"}
    assert get_json_field_from_response(mock_resp, "token") == "abc"

def test_get_json_field_from_response_invalid_json():
    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.json.side_effect = Exception("invalid")
    assert get_json_field_from_response(mock_resp, "token") is None

def test_get_data_field_from_response_found():
    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.json.return_value = {"data": {"uid": 456}}
    assert get_data_field_from_response(mock_resp, "uid") == 456

def test_get_data_field_from_response_not_found():
    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.json.return_value = {"data": {}}
    assert get_data_field_from_response(mock_resp, "uid") is None

def test_get_token_from_response_found():
    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.json.return_value = {"data": {"token": "xyz"}}
    assert get_token_from_response(mock_resp) == "xyz"

def test_get_token_from_response_invalid():
    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.json.side_effect = Exception("boom")
    assert get_token_from_response(mock_resp) is None

def test_get_error_message_from_response_msg():
    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.json.return_value = {"msg": "錯誤訊息"}
    assert get_error_message_from_response(mock_resp) == "錯誤訊息"

def test_get_error_message_from_response_error():
    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.json.return_value = {"error": "失敗原因"}
    assert get_error_message_from_response(mock_resp) == "失敗原因"

def test_get_error_message_from_response_invalid_json():
    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.json.side_effect = Exception("invalid json")
    assert get_error_message_from_response(mock_resp) == "回傳格式錯誤"
