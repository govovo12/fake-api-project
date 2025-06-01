from workspace.utils.notifier.telegram_notifier import TelegramNotifier

class NotifierFactory:
    """
    [TOOL] Notifier 工廠：依參數產生對應通知工具。
    """
    is_tool = True   # tools 掃描用

    @staticmethod
    def get_notifier(token: str, chat_id: str):
        """產生 TelegramNotifier，未來可擴充多平台"""
        return TelegramNotifier(token, chat_id)
