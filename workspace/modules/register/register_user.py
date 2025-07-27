# 📦 共用錯誤碼
from workspace.config.rules.error_codes import ResultCode

# 📂 路徑與工具
from workspace.config.paths import get_user_path
from workspace.utils.data.data_loader import load_json
from workspace.utils.request.request_handler import post
from workspace.utils.response.response_helper import get_status_code_from_response
from dotenv import load_dotenv
load_dotenv()  # 確保載入 .env

import os

def register_user(uuid: str, url: str, headers: dict) -> int:
    """
    註冊 Fake Store API 使用者
    """
    path = get_user_path(uuid)
    payload = load_json(path)

    if not isinstance(payload, dict):
        return payload

    debug = os.getenv("DEBUG_API_LOG") == "1"

    try:
        if debug:
            print("[DEBUG] 🔗 註冊 URL:", url)
            print("[DEBUG] 🧾 headers:", headers)
            print("[DEBUG] 📝 payload:", payload)

        response = post(url=url, headers=headers, json=payload)
        status = get_status_code_from_response(response)

        if debug:
            print("[DEBUG] 📬 status_code:", response.status_code)
            print("[DEBUG] 📦 response body:", response.text)

        if status in (200, 201):
            return 0
        return ResultCode.FAKER_REGISTER_FAILED
    except Exception as e:
        if debug:
            print("[DEBUG] 💥 Exception:", e)
        return ResultCode.FAKER_REGISTER_EXCEPTION

