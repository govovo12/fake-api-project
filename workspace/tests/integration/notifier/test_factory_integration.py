import pytest
from unittest.mock import patch, MagicMock

from workspace.utils.notifier.factory import NotifierFactory
from workspace.utils.notifier.telegram_notifier import TelegramNotifier

pytestmark = [pytest.mark.integration, pytest.mark.notifier]


class TestNotifierFactoryIntegration:
    def test_factory_creates_notifier_and_sends_message(self):
        """✅ 整合測試：由工廠產出 notifier 並成功發送訊息"""
        fake_token = "fake-token"
        fake_chat_id = "987654321"

        with patch("workspace.utils.notifier.telegram_notifier.requests.post") as mock_post:
            mock_response = MagicMock(status_code=200, json=lambda: {"ok": True})
            mock_post.return_value = mock_response

            notifier = NotifierFactory.get_notifier(fake_token, fake_chat_id)

            assert isinstance(notifier, TelegramNotifier)
            result = notifier.send("Integration test from factory")
            assert result is True
            mock_post.assert_called_once()

    def test_factory_returns_none_with_missing_values(self):
        """❌ 整合測試：參數不完整時應回傳 None"""
        assert NotifierFactory.get_notifier(None, "123") is None
        assert NotifierFactory.get_notifier("abc", None) is None
