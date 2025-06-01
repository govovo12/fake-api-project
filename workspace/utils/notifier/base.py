from abc import ABC, abstractmethod

class Notifier(ABC):
    """
    [TOOL] 抽象通知介面：所有通知模組（如 Telegram/Slack/Email）皆應繼承。
    僅規範 send(message: str) 方法，保持單一職責。
    """
    @abstractmethod
    def send(self, message: str) -> bool:
        """發送通知訊息，成功回傳 True，失敗回傳 False"""
        pass
