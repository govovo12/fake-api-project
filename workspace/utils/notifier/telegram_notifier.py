import os
import requests

class TelegramNotifier:
    def __init__(self, token: str = None, chat_id: str = None):
        # 預設會自動讀取 os.environ（從 .env 或環境變數）
        self.token = token or os.getenv("TG_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TG_CHAT_ID")
        self.send_url = f"https://api.telegram.org/bot{self.token}/sendMessage" if self.token else None

    def send(self, message: str):
        # 這行能同時擋 None、空字串、全空白字串
        if not self.token or not self.chat_id or not str(self.token).strip() or not str(self.chat_id).strip():
            print("[Notifier] Telegram token 或 chat_id 未設定，跳過發送。")
            return False

        payload = {
            "chat_id": self.chat_id,
            "text": message
        }

        try:
            response = requests.post(self.send_url, json=payload, timeout=5)
            if response.status_code == 200:
                return True
            else:
                print(f"[Notifier] 發送失敗：{response.status_code}, {response.text}")
                return False
        except Exception as e:
            print(f"[Notifier] 發送例外：{e}")
            return False
