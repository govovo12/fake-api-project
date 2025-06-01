import pytest
import requests
from utils.request import request_handler
from utils.mock.mock_helper import mock_api_response

pytestmark = [pytest.mark.unit, pytest.mark.request]

def test_get_success(monkeypatch):
    """[GET] 成功 200，回傳正確 Response"""
    monkeypatch.setattr(
        "utils.request.request_handler.requests.get",
        lambda *args, **kwargs: mock_api_response(status_code=200, json_data={"ok": True})
    )
    res = request_handler.get("https://test.com")
    assert res.status_code == 200
    assert res.json() == {"ok": True}

def test_get_not_found(monkeypatch):
    """[GET] 404 Not Found，回傳正確 Response"""
    monkeypatch.setattr(
        "utils.request.request_handler.requests.get",
        lambda *args, **kwargs: mock_api_response(status_code=404)
    )
    res = request_handler.get("https://test.com/missing")
    assert res.status_code == 404

def test_get_raises_request_exception(monkeypatch):
    """[GET] 發生 requests.RequestException 時正確拋出"""
    def raise_exc(*args, **kwargs):
        raise requests.RequestException("network error")
    monkeypatch.setattr(
        "utils.request.request_handler.requests.get",
        raise_exc
    )
    with pytest.raises(requests.RequestException):
        request_handler.get("https://test.com/error")

def test_post_success_created(monkeypatch):
    """[POST] 201 Created，回傳正確 Response"""
    monkeypatch.setattr(
        "utils.request.request_handler.requests.post",
        lambda *args, **kwargs: mock_api_response(status_code=201, json_data={"created": True})
    )
    res = request_handler.post("https://test.com", json={"k": "v"})
    assert res.status_code == 201
    assert res.json() == {"created": True}

def test_post_fail(monkeypatch):
    """[POST] 500 失敗，回傳正確 Response"""
    monkeypatch.setattr(
        "utils.request.request_handler.requests.post",
        lambda *args, **kwargs: mock_api_response(status_code=500)
    )
    res = request_handler.post("https://test.com", json={"k": "v"})
    assert res.status_code == 500

def test_post_raises_request_exception(monkeypatch):
    """[POST] 發生 requests.RequestException 時正確拋出"""
    def raise_exc(*args, **kwargs):
        raise requests.RequestException("network error")
    monkeypatch.setattr(
        "utils.request.request_handler.requests.post",
        raise_exc
    )
    with pytest.raises(requests.RequestException):
        request_handler.post("https://test.com", json={"k": "v"})
