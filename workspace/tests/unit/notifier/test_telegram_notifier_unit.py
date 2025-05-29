# workspace/tests/unit/notifier/test_telegram_notifier_unit.py

import pytest
import requests
from utils.notifier.telegram_notifier import TelegramNotifier
from utils.mock.mock_helper import mock_api_response

pytestmark = [pytest.mark.unit, pytest.mark.notifier]

@pytest.fixture
def telegram_notifier():
    return TelegramNotifier(token="TEST_TOKEN", chat_id="TEST_CHAT")

def test_send_success(monkeypatch):
    # 成功回傳 200
    monkeypatch.setattr(
        "utils.notifier.telegram_notifier.requests.post",
        lambda *args, **kwargs: mock_api_response(status_code=200)
    )
    notifier = TelegramNotifier(token="TEST_TOKEN", chat_id="TEST_CHAT")
    assert notifier.send("hello") is True

def test_send_fail(monkeypatch):
    # 失敗回傳 500
    monkeypatch.setattr(
        "utils.notifier.telegram_notifier.requests.post",
        lambda *args, **kwargs: mock_api_response(status_code=500)
    )
    notifier = TelegramNotifier(token="TEST_TOKEN", chat_id="TEST_CHAT")
    assert notifier.send("hello") is False

def test_send_raises_request_exception(monkeypatch, capsys):
    # 模擬網路例外
    def raise_exc(*args, **kwargs):
        raise requests.RequestException("network error")
    monkeypatch.setattr(
        "utils.notifier.telegram_notifier.requests.post",
        raise_exc
    )
    notifier = TelegramNotifier(token="TEST_TOKEN", chat_id="TEST_CHAT")
    # send 應捕獲例外並回傳 False，而不是拋出
    result = notifier.send("hello")
    assert result is False

    out = capsys.readouterr().out
    assert "[Notifier] 發送例外" in out
