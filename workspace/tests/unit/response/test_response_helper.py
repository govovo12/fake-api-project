import pytest
import requests
from unittest.mock import MagicMock
from workspace.utils.response.response_helper import (
    is_register_success_dict,
    get_json_field_from_response,
    extract_token_from_dict,
    get_error_message_from_dict,
)


pytestmark = [pytest.mark.unit, pytest.mark.response]

# 測試判斷回應是否成功
def test_is_success_dict_true():
    resp = {"code": 200, "data": {"token": "abc"}}
    assert is_success_dict(resp) is True

def test_is_success_dict_false():
    resp = {"code": 400, "msg": "error"}
    assert is_success_dict(resp) is False

# 測試從回應中擷取 token
def test_extract_token_from_dict():
    resp = {"data": {"token": "xyz"}}
    assert extract_token_from_dict(resp) == "xyz"

def test_extract_token_from_dict_missing():
    resp = {"data": {}}
    assert extract_token_from_dict(resp) == ""

# 測試擷取錯誤訊息
def test_get_error_message_from_dict_msg():
    resp = {"msg": "錯誤訊息"}
    assert get_error_message_from_dict(resp) == "錯誤訊息"

def test_get_error_message_from_dict_error():
    resp = {"error": "失敗原因"}
    assert get_error_message_from_dict(resp) == "失敗原因"

def test_get_error_message_from_dict_fallback():
    resp = {}
    assert get_error_message_from_dict(resp) == "未知錯誤"

# 測試擷取 data 欄位的指定欄位
def test_get_data_field_from_dict_found():
    resp = {"data": {"uid": 123}}
    assert get_data_field_from_dict(resp, "uid") == 123

def test_get_data_field_from_dict_not_found():
    resp = {"data": {}}
    assert get_data_field_from_dict(resp, "uid") is None

# 測試註冊是否成功
def test_is_register_success_dict_true():
    resp = {"id": 1}
    assert is_register_success_dict(resp) is True

def test_is_register_success_dict_false():
    resp = {"msg": "fail"}
    assert is_register_success_dict(resp) is False

# 測試從 requests.Response 擷取 json 欄位
def test_get_json_field_from_response_success():
    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.json.return_value = {"token": "abc"}
    assert get_json_field_from_response(mock_resp, "token") == "abc"

def test_get_json_field_from_response_invalid_json():
    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.json.side_effect = Exception("invalid")
    assert get_json_field_from_response(mock_resp, "token") is None
