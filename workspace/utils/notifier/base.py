from abc import ABC, abstractmethod

class Notifier(ABC):
    """
    抽象通知介面：所有通知模組（如 Telegram、Slack）皆應繼承此類別，
    並實作 send(message: str) 方法，用以實現跨模組的統一調用方式。
    適用於展示作品中展現程式設計抽象化與擴充能力。
    """

    @abstractmethod
    def send(self, message: str):
        """發送通知訊息"""
        pass