import pytest
from utils.notifier.telegram_notifier import TelegramNotifier

pytestmark = [pytest.mark.unit, pytest.mark.notifier]

def test_send_success(monkeypatch):
    """[SUCCESS] 發送成功時應回傳 True"""
    class FakeResponse:
        status_code = 200
    def fake_post(url, json, timeout):
        assert "chat_id" in json and "text" in json
        return FakeResponse()
    monkeypatch.setattr("utils.notifier.telegram_notifier.requests.post", fake_post)
    notifier = TelegramNotifier("FAKE_TOKEN", "FAKE_CHAT_ID")
    assert notifier.send("測試訊息") is True

def test_send_fail_http(monkeypatch):
    """[FAIL] 發送失敗 (非 200 status_code) 應回傳 False"""
    class FakeResponse:
        status_code = 400
    monkeypatch.setattr(
        "utils.notifier.telegram_notifier.requests.post",
        lambda url, json, timeout: FakeResponse()
    )
    notifier = TelegramNotifier("FAKE_TOKEN", "FAKE_CHAT_ID")
    assert notifier.send("訊息") is False

def test_send_fail_exception(monkeypatch):
    """[FAIL] 發送時遇 Exception 應回傳 False"""
    def fake_post(url, json, timeout):
        raise Exception("network error")
    monkeypatch.setattr("utils.notifier.telegram_notifier.requests.post", fake_post)
    notifier = TelegramNotifier("FAKE_TOKEN", "FAKE_CHAT_ID")
    assert notifier.send("錯誤訊息") is False

def test_send_missing_token_or_chat_id():
    """[EDGE] 缺 token 或 chat_id 應直接回傳 False（不發送）"""
    notifier = TelegramNotifier("", "123")
    assert notifier.send("msg") is False
    notifier = TelegramNotifier("T", "")
    assert notifier.send("msg") is False
    notifier = TelegramNotifier("", "")
    assert notifier.send("msg") is False
