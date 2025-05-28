import requests

class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.send_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send(self, message: str):
        if not self.token or not self.chat_id:
            print("[Notifier] Telegram token 或 chat_id 未設定，跳過發送。")
            return False  # 建議明確回 False，方便測試 assert

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
