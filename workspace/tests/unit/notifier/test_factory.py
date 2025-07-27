import pytest
from workspace.utils.notifier.factory import NotifierFactory
from workspace.utils.notifier.telegram_notifier import TelegramNotifier

pytestmark = [pytest.mark.unit, pytest.mark.notifier]


class TestNotifierFactory:
    def test_create_telegram_notifier_success(self):
        """✅ 產生合法 TelegramNotifier 實體"""
        token = "fake-token"
        chat_id = "123456789"
        notifier = NotifierFactory.get_notifier(token, chat_id)

        assert isinstance(notifier, TelegramNotifier)
        assert notifier.token == token
        assert notifier.chat_id == chat_id

    def test_create_telegram_notifier_missing_token(self):
        """❌ 無 token，應回傳 None"""
        notifier = NotifierFactory.get_notifier(None, "123456")
        assert notifier is None

    def test_create_telegram_notifier_missing_chat_id(self):
        """❌ 無 chat_id，應回傳 None"""
        notifier = NotifierFactory.get_notifier("abc123", None)
        assert notifier is None

    def test_create_telegram_notifier_missing_both(self):
        """❌ token 和 chat_id 都無，應回傳 None"""
        notifier = NotifierFactory.get_notifier(None, None)
        assert notifier is None
