import os
import pytest
from workspace.utils.notifier.factory import NotifierFactory
from dotenv import load_dotenv
load_dotenv()

pytestmark = [pytest.mark.e2e, pytest.mark.notifier]


def test_send_real_message_from_factory():
    """🚀 真實發送訊息：從工廠建立 notifier 並發送 Telegram 訊息"""
    token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")

    assert token, "❌ .env 中缺少 TG_BOT_TOKEN"
    assert chat_id, "❌ .env 中缺少 TG_CHAT_ID"

    notifier = NotifierFactory.get_notifier(token, chat_id)
    assert notifier is not None, "❌ 無法產生 Notifier 實體"

    message = "✅ 測試通知成功：E2E from GitHub pipeline"
    success = notifier.send(message)
    assert success, "❌ 訊息發送失敗"
