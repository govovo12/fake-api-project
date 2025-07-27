from dotenv import load_dotenv
load_dotenv()

import os
import requests
from datetime import datetime


def get_ci_result_summary() -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_url = os.getenv("GITHUB_PAGES_URL", "🔗 GitHub Pages 尚未設定")
    ci_status = os.getenv("CI_TEST_STATUS", "unknown")

    status_emoji = {
        "success": "✅ 測試通過",
        "failure": "❌ 測試失敗"
    }.get(ci_status, "⚠️ 狀態未知")

    return (
        f"{status_emoji}\n"
        f"🕒 時間：{now}\n"
        f"📄 報告總覽：{report_url}/index.html"
    )


def send_tg_message(text: str):
    # ✅ 同時支援 TELEGRAM_* 與 TG_* 命名
    token = os.getenv("TELEGRAM_TOKEN") or os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID") or os.getenv("TG_CHAT_ID")

    if not token or not chat_id:
        print("❌ TELEGRAM_TOKEN / TG_BOT_TOKEN 未設定")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=payload)

    if response.status_code != 200:
        print(f"❌ 發送 Telegram 訊息失敗：{response.text}")


if __name__ == "__main__":
    message = get_ci_result_summary()
    send_tg_message(message)
