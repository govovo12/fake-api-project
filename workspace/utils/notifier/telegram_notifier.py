import requests
from workspace.utils.notifier.base import Notifier

class TelegramNotifier(Notifier):
    """
    [TOOL] Telegram 發送通知
    - 只負責發送，不主動 log/env/重試
    """
    is_tool = True   # tools 掃描用

    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.send_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send(self, message: str) -> bool:
        if not self.token or not self.chat_id:
            return False
        payload = {"chat_id": self.chat_id, "text": message}
        try:
            resp = requests.post(self.send_url, json=payload, timeout=5)
            return resp.status_code == 200
        except Exception:
            return False
