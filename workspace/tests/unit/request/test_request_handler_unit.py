import pytest
from unittest.mock import patch, MagicMock
from utils.request import request_handler

pytestmark = [pytest.mark.unit, pytest.mark.request]



@patch("utils.request.request_handler.requests.get")
def test_get_success(mock_get, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.ok = True
    mock_get.return_value = mock_response

    res = request_handler.get("https://test.com")

    assert res.status_code == 200
    captured = capsys.readouterr().out
    assert "[GET]" in captured
    assert "→ 200" in captured


@patch("utils.request.request_handler.requests.post")
def test_post_fail_and_log_error(mock_post, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.ok = False
    mock_post.return_value = mock_response

    res = request_handler.post("https://test.com", json={"k": "v"})

    assert res.status_code == 500
    captured = capsys.readouterr().out
    assert "[POST]" in captured
    assert "→ 500" in captured
