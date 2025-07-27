"""
📦 工廠模組：根據參數產出對應的通知工具
"""

from workspace.utils.notifier.telegram_notifier import TelegramNotifier


class NotifierFactory:
    @staticmethod
    def get_notifier(token: str, chat_id: str):
        """產生 TelegramNotifier，未來可擴充多平台"""
        if not token or not chat_id:
            return None
        return TelegramNotifier(token, chat_id)