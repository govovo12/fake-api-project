import pytest
import requests
from utils.request import request_handler
from utils.mock.mock_helper import mock_api_response
from unittest.mock import MagicMock

pytestmark = [pytest.mark.unit, pytest.mark.request]

# === 測試 GET ===

def test_get_success(monkeypatch):
    monkeypatch.setattr(
        "utils.request.request_handler.requests.get",
        lambda *args, **kwargs: mock_api_response(status_code=200, json_data={"ok": True})
    )
    res = request_handler.get("https://test.com")
    assert res.status_code == 200
    assert res.json() == {"ok": True}

def test_get_not_found(monkeypatch):
    monkeypatch.setattr(
        "utils.request.request_handler.requests.get",
        lambda *args, **kwargs: mock_api_response(status_code=404)
    )
    res = request_handler.get("https://test.com/missing")
    assert res.status_code == 404

def test_get_raises_request_exception(monkeypatch):
    def raise_exc(*args, **kwargs):
        raise requests.RequestException("network error")
    monkeypatch.setattr(
        "utils.request.request_handler.requests.get",
        raise_exc
    )
    with pytest.raises(requests.RequestException):
        request_handler.get("https://test.com/error")

# === 測試 POST ===

def test_post_success_created(monkeypatch):
    monkeypatch.setattr(
        "utils.request.request_handler.requests.post",
        lambda *args, **kwargs: mock_api_response(status_code=201, json_data={"created": True})
    )
    res = request_handler.post("https://test.com", json={"k": "v"})
    assert res.status_code == 201
    assert res.json() == {"created": True}

def test_post_fail(monkeypatch):
    monkeypatch.setattr(
        "utils.request.request_handler.requests.post",
        lambda *args, **kwargs: mock_api_response(status_code=500)
    )
    res = request_handler.post("https://test.com", json={"k": "v"})
    assert res.status_code == 500

def test_post_raises_request_exception(monkeypatch):
    def raise_exc(*args, **kwargs):
        raise requests.RequestException("network error")
    monkeypatch.setattr(
        "utils.request.request_handler.requests.post",
        raise_exc
    )
    with pytest.raises(requests.RequestException):
        request_handler.post("https://test.com", json={"k": "v"})

# === 測試 parse_json_safe ===

def test_parse_json_safe_success():
    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.json.return_value = {"a": 123}
    success, data = request_handler.parse_json_safe(mock_resp)
    assert success is True
    assert data == {"a": 123}

def test_parse_json_safe_fail():
    mock_resp = MagicMock(spec=requests.Response)
    mock_resp.json.side_effect = Exception("invalid json")
    success, data = request_handler.parse_json_safe(mock_resp)
    assert success is False
    assert data is None

# === 測試 post_and_parse_json ===

def test_post_and_parse_json_success(monkeypatch):
    def mock_post(*args, **kwargs):
        return mock_api_response(status_code=200, json_data={"msg": "ok"})
    monkeypatch.setattr(
        "utils.request.request_handler.requests.post",
        mock_post
    )
    code, json_data = request_handler.post_and_parse_json("https://test.com", payload={"a": 1})
    assert code == 200
    assert json_data == {"msg": "ok"}

def test_post_and_parse_json_invalid_json(monkeypatch):
    def mock_post(*args, **kwargs):
        mock = mock_api_response(status_code=200)
        mock.json.side_effect = Exception("invalid json")
        return mock
    monkeypatch.setattr(
        "utils.request.request_handler.requests.post",
        mock_post
    )
    code, json_data = request_handler.post_and_parse_json("https://test.com", payload={"a": 1})
    assert code == 200
    assert json_data is None
