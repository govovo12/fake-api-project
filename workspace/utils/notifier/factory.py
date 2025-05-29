from workspace.utils.notifier.telegram_notifier import TelegramNotifier

class NotifierFactory:
    @staticmethod
    def get_notifier():
        # 完全不需要傳參數，讓 telegram_notifier.py 自己用 os.environ 取
        return TelegramNotifier()
