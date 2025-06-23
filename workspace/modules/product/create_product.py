"""
建立商品任務模組：讀取測資檔並呼叫 API 建立商品。
此模組屬於任務層級，負責：
- 根據 UUID 讀取商品測資 JSON
- 組裝 API 請求資料並發送建立商品請求
- 回傳 ResultCode 與回應內容（若有）
"""

# ------------------------
# 📦 錯誤碼與配置
# ------------------------
from workspace.config.rules.error_codes import ResultCode
from workspace.config.paths import (
    get_product_path,
    get_create_product_url,
    get_headers,
)

# ------------------------
# 🧰 工具模組
# ------------------------
from workspace.utils.data.data_loader import load_json
from workspace.utils.request.request_handler import post_and_parse_json

# ------------------------
# ✨ 型別標註（如有需要）
# ------------------------
from typing import Tuple


def create_product(uuid: str, token: str = "") -> tuple[int, dict | None]:
    """
    根據指定 UUID 讀取測資檔案，並發送建立商品 API 請求。

    Args:
        uuid (str): 商品測資檔案的 UUID（對應本地 JSON 檔案）
        token (str): 可選的 Bearer token（預設為空，Fake Store API 不驗證）

    Returns:
        tuple[int, dict | None]: 回傳一個 tuple，包含：
            - ResultCode（int）
            - 回應資料（dict，若失敗則為 None）
    """
    # 組合測資檔案路徑並讀取 JSON 內容
    path = get_product_path(uuid)
    payload = load_json(path)

    # 若讀取失敗或資料型別不正確，回傳錯誤
    if not isinstance(payload, dict):
        return ResultCode.TOOL_FILE_LOAD_FAILED, None

    # 準備 API 請求資訊
    url = get_create_product_url()
    headers = get_headers()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    # 發送 POST 請求並解析結果
    try:
        status_code, response = post_and_parse_json(url, payload, headers)
    except Exception:
        return ResultCode.REQUESTS_EXCEPTION, None

    # 根據回傳狀態碼決定回傳的錯誤碼
    if status_code == 200:
        return ResultCode.SUCCESS, response  
    elif 500 <= status_code < 600:
        return ResultCode.SERVER_ERROR, response
    else:
        return ResultCode.CREATE_PRODUCT_FAILED, response
