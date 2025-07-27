import pytest
from unittest.mock import patch, MagicMock

from workspace.utils.notifier.telegram_notifier import TelegramNotifier

pytestmark = [pytest.mark.integration, pytest.mark.notifier]


class TestTelegramNotifierIntegration:
    def test_send_success_real_scenario(self):
        """✅ 模擬實際送出成功（整合測試）"""
        with patch("workspace.utils.notifier.telegram_notifier.requests.post") as mock_post:
            mock_response = MagicMock(status_code=200, json=lambda: {"ok": True})
            mock_post.return_value = mock_response

            notifier = TelegramNotifier(token="fake-token", chat_id="123456789")
            result = notifier.send("This is a test integration message")

            mock_post.assert_called_once()
            assert result is True

    def test_send_fail_invalid_token(self):
        """❌ 模擬錯誤 token 導致失敗（整合測試）"""
        with patch("workspace.utils.notifier.telegram_notifier.requests.post") as mock_post:
            mock_response = MagicMock(status_code=401)
            mock_post.return_value = mock_response

            notifier = TelegramNotifier(token="invalid-token", chat_id="123456789")
            result = notifier.send("Should fail")

            assert result is False
