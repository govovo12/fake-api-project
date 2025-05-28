import pytest
from unittest.mock import patch, Mock
from workspace.utils.notifier.telegram_notifier import TelegramNotifier

pytestmark = pytest.mark.notifier

def test_init_notifier():
    notifier = TelegramNotifier(token="dummy_token", chat_id="dummy_chat")
    assert notifier.token == "dummy_token"
    assert notifier.chat_id == "dummy_chat"

def test_send_success():
    notifier = TelegramNotifier(token="t", chat_id="c")
    with patch("requests.post") as mock_post:
        mock_post.return_value = Mock(status_code=200)
        notifier.send("hi")
        mock_post.assert_called_once()

def test_send_fail_status():
    notifier = TelegramNotifier(token="t", chat_id="c")
    with patch("requests.post") as mock_post:
        mock_post.return_value = Mock(status_code=500, text="Internal Error")
        notifier.send("fail")
        mock_post.assert_called_once()

def test_send_exception():
    notifier = TelegramNotifier(token="t", chat_id="c")
    with patch("requests.post", side_effect=Exception("Network error")) as mock_post:
        notifier.send("error")
        mock_post.assert_called_once()

def test_send_skipped_if_no_config():
    notifier = TelegramNotifier(token=None, chat_id=None)
    with patch("requests.post") as mock_post:
        notifier.send("should not send")
        mock_post.assert_not_called()
