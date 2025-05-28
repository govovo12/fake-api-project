# workspace/tests/integration/notifier/test_notifier_controller_integration.py
import pytest
from unittest.mock import patch
from workspace.utils.notifier.factory import NotifierFactory

pytestmark = pytest.mark.notifier


def test_factory_provides_telegram_notifier():
    with patch("workspace.utils.env.env_manager.load_env") as mock_load_env, \
         patch("workspace.utils.env.env_manager.get_env") as mock_get_env:
        mock_load_env.return_value = None
        mock_get_env.side_effect = lambda key, default="": {
            "TG_BOT_TOKEN": "fake-token",
            "TG_CHAT_ID": "fake-chat-id"
        }.get(key, default)

        notifier = NotifierFactory.get_notifier()
        assert notifier is not None
        assert hasattr(notifier, "send")


def test_factory_send_success():
    with patch("workspace.utils.env.env_manager.load_env") as mock_load_env, \
         patch("workspace.utils.env.env_manager.get_env") as mock_get_env, \
         patch("requests.post") as mock_post:
        mock_load_env.return_value = None
        mock_get_env.side_effect = lambda key, default="": {
            "TG_BOT_TOKEN": "fake-token",
            "TG_CHAT_ID": "fake-chat-id"
        }.get(key, default)
        mock_post.return_value.ok = True
        mock_post.return_value.status_code = 200   # ★★★ 加這行最關鍵 ★★★
        mock_post.return_value.text = "OK"         # 避免你 code print 出現亂碼
        mock_post.return_value.json.return_value = {"ok": True}

        notifier = NotifierFactory.get_notifier()
        assert notifier.send("測試訊息") is True

