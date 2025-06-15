import pytest
import requests
from workspace.utils.request.request_handler import get, post, post_and_parse_json
from workspace.utils.mock.mock_helper import mock_api_response


@pytest.mark.unit
@pytest.mark.request
def test_get_success(monkeypatch):
    """
    ✅ 測試 GET 成功（200 回傳）
    """
    def mock_get(*args, **kwargs):
        return mock_api_response(status_code=200)

    monkeypatch.setattr("requests.get", mock_get)
    res = get("https://example.com")
    assert res.status_code == 200


@pytest.mark.unit
@pytest.mark.request
def test_post_success_created(monkeypatch):
    """
    ✅ 測試 POST 成功（201 Created）
    """
    def mock_post(url, headers, json=None, **kwargs):
        return mock_api_response(status_code=201)

    monkeypatch.setattr("requests.post", mock_post)
    res = post("https://example.com", headers={"Content-Type": "application/json"})
    assert res.status_code == 201


@pytest.mark.unit
@pytest.mark.request
def test_post_fail(monkeypatch):
    """
    ❌ 測試 POST 回傳 404（非成功）
    """
    def mock_post(url, headers, json=None, **kwargs):
        return mock_api_response(status_code=404)

    monkeypatch.setattr("requests.post", mock_post)
    res = post("https://example.com", headers={"Content-Type": "application/json"})
    assert res.status_code == 404


@pytest.mark.unit
@pytest.mark.request
def test_post_raises_request_exception(monkeypatch):
    """
    💥 模擬 POST 發生例外（例如 timeout）
    """
    def mock_post(url, headers, json=None, **kwargs):
        raise requests.exceptions.RequestException("API failed")

    monkeypatch.setattr("requests.post", mock_post)

    with pytest.raises(requests.exceptions.RequestException):
        post("https://example.com", headers={"Content-Type": "application/json"})


@pytest.mark.unit
@pytest.mark.request
def test_post_and_parse_json_success(monkeypatch):
    """
    ✅ 測試 post_and_parse_json 成功解析 JSON 回傳
    """
    def mock_post(url, headers, json=None, **kwargs):
        return mock_api_response(status_code=200, json_data={"message": "OK"})

    monkeypatch.setattr("workspace.utils.request.request_handler.post", mock_post)
    status, result = post_and_parse_json("https://example.com", headers={}, payload={})
    assert status == 200
    assert result == {"message": "OK"}




@pytest.mark.unit
@pytest.mark.request
def test_post_and_parse_json_invalid_json(monkeypatch):
    """
    ❌ 模擬回傳內容無法解析為 JSON（觸發例外）
    """
    def mock_post(url, headers, json=None, **kwargs):
        mock = mock_api_response(status_code=200)
        mock.json.side_effect = Exception("invalid json")
        return mock

    monkeypatch.setattr("workspace.utils.request.request_handler.post", mock_post)
    status, result = post_and_parse_json("https://example.com", headers={}, payload={})
    assert status == 200
    assert result is None


