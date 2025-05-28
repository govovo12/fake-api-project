from workspace.utils.env.env_manager import load_env, get_env
from workspace.utils.notifier.telegram_notifier import TelegramNotifier


class NotifierFactory:
    @staticmethod
    def get_notifier():
        """
        回傳實作的 Notifier 物件，目前僅支援 Telegram
        """
        load_env("telegram.env")
        token = get_env("TG_BOT_TOKEN")
        chat_id = get_env("TG_CHAT_ID")
        return TelegramNotifier(token=token, chat_id=chat_id)
