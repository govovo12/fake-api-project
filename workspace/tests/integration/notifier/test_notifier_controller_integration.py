import pytest
from workspace.utils.notifier.factory import NotifierFactory

pytestmark = pytest.mark.notifier

def test_factory_provides_telegram_notifier(monkeypatch):
    monkeypatch.setenv("TG_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TG_CHAT_ID", "test-chat")
    notifier = NotifierFactory.get_notifier()
    assert notifier is not None
    assert hasattr(notifier, "send")

def test_factory_send_success(monkeypatch):
    monkeypatch.setenv("TG_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TG_CHAT_ID", "test-chat")
    from unittest.mock import patch, Mock
    with patch("requests.post") as mock_post:
        mock_post.return_value = Mock(status_code=200)
        notifier = NotifierFactory.get_notifier()
        assert notifier.send("測試訊息") is True
        mock_post.assert_called_once()

def test_factory_send_fail_status(monkeypatch):
    monkeypatch.setenv("TG_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TG_CHAT_ID", "test-chat")
    from unittest.mock import patch, Mock
    with patch("requests.post") as mock_post:
        mock_post.return_value = Mock(status_code=500, text="Error")
        notifier = NotifierFactory.get_notifier()
        assert notifier.send("fail") is False
        mock_post.assert_called_once()

def test_factory_send_fail_no_config(monkeypatch):
    monkeypatch.delenv("TG_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TG_CHAT_ID", raising=False)
    notifier = NotifierFactory.get_notifier()
    assert notifier.send("config missing") is False
