import pytest
import requests
from unittest.mock import patch, MagicMock

from workspace.utils.notifier.telegram_notifier import TelegramNotifier

pytestmark = [pytest.mark.unit, pytest.mark.notifier]


class TestTelegramNotifier:
    def test_send_success(self):
        """✅ 成功發送 Telegram 訊息"""
        with patch("workspace.utils.notifier.telegram_notifier.requests.post") as mock_post:
            mock_response = MagicMock(status_code=200, json=lambda: {"ok": True})
            mock_post.return_value = mock_response

            notifier = TelegramNotifier(token="fake-token", chat_id="12345")
            result = notifier.send("Hello, world!")

            mock_post.assert_called_once()
            assert result is True

    def test_send_failure_due_to_status_code(self):
        """❌ 發送失敗：回傳非 200 狀態碼"""
        with patch("workspace.utils.notifier.telegram_notifier.requests.post") as mock_post:
            mock_post.return_value = MagicMock(status_code=500)

            notifier = TelegramNotifier(token="fake-token", chat_id="12345")
            result = notifier.send("Failed message")

            assert result is False

    def test_send_failure_due_to_missing_token(self):
        """❌ 發送失敗：token 缺失"""
        notifier = TelegramNotifier(token=None, chat_id="12345")
        result = notifier.send("Missing token")
        assert result is False

    def test_send_failure_due_to_missing_chat_id(self):
        """❌ 發送失敗：chat_id 缺失"""
        notifier = TelegramNotifier(token="abc123", chat_id=None)
        result = notifier.send("Missing chat_id")
        assert result is False
