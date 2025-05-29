# workspace/tests/unit/request/test_request_handler_unit.py

import pytest
import requests
from utils.request import request_handler
from utils.mock.mock_helper import mock_api_response

pytestmark = [pytest.mark.unit, pytest.mark.request]

def test_get_success(monkeypatch, capsys):
    # 成功 (200)
    monkeypatch.setattr(
        "utils.request.request_handler.requests.get",
        lambda *args, **kwargs: mock_api_response(status_code=200, json_data={"ok": True})
    )
    res = request_handler.get("https://test.com")
    assert res.status_code == 200

    out = capsys.readouterr().out
    assert "[GET]" in out and "→ 200" in out

def test_get_not_found(monkeypatch, capsys):
    # 未找到 (404)
    monkeypatch.setattr(
        "utils.request.request_handler.requests.get",
        lambda *args, **kwargs: mock_api_response(status_code=404)
    )
    res = request_handler.get("https://test.com/missing")
    assert res.status_code == 404

    out = capsys.readouterr().out
    assert "[GET]" in out and "→ 404" in out

def test_get_raises_request_exception(monkeypatch):
    # 模擬網路例外
    def raise_exc(*args, **kwargs):
        raise requests.RequestException("network error")
    monkeypatch.setattr(
        "utils.request.request_handler.requests.get",
        raise_exc
    )
    with pytest.raises(requests.RequestException):
        request_handler.get("https://test.com/error")

def test_post_success_created(monkeypatch, capsys):
    # 成功建立 (201)
    monkeypatch.setattr(
        "utils.request.request_handler.requests.post",
        lambda *args, **kwargs: mock_api_response(status_code=201, json_data={"created": True})
    )
    res = request_handler.post("https://test.com", json={"k": "v"})
    assert res.status_code == 201

    out = capsys.readouterr().out
    assert "[POST]" in out and "→ 201" in out

def test_post_fail_and_log_error(monkeypatch, capsys):
    # 失敗 (500)
    monkeypatch.setattr(
        "utils.request.request_handler.requests.post",
        lambda *args, **kwargs: mock_api_response(status_code=500)
    )
    res = request_handler.post("https://test.com", json={"k": "v"})
    assert res.status_code == 500

    out = capsys.readouterr().out
    assert "[POST]" in out and "→ 500" in out

def test_post_raises_request_exception(monkeypatch):
    # 模擬網路例外
    def raise_exc(*args, **kwargs):
        raise requests.RequestException("network error")
    monkeypatch.setattr(
        "utils.request.request_handler.requests.post",
        raise_exc
    )
    with pytest.raises(requests.RequestException):
        request_handler.post("https://test.com", json={"k": "v"})
