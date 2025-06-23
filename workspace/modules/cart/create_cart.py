"""
建立購物車任務模組：依據 UUID 載入測資並建立購物車。
"""

# ------------------------
# 📦 錯誤碼與配置
# ------------------------
from workspace.config.rules.error_codes import ResultCode
from workspace.config.paths import get_cart_path, get_create_cart_url, get_headers

# ------------------------
# 🧰 工具模組
# ------------------------
from workspace.utils.data.data_loader import load_json
from workspace.utils.request.request_handler import post_and_parse_json


def create_cart(uuid: str, token: str) -> tuple[int, dict]:
    """
    建立購物車測試資料：
    - 根據 UUID 載入 JSON 測資
    - 發送帶有 Bearer Token 的 POST 請求至 /carts
    - 根據回傳狀態碼給出對應錯誤碼

    Args:
        uuid (str): 測資檔 UUID
        token (str): Bearer token

    Returns:
        tuple[int, dict]: (錯誤碼 or SUCCESS, 回應內容 or 空字典)
    """
    try:
        path = get_cart_path(uuid)
        payload = load_json(path)
    except Exception:
        return ResultCode.TOOL_FILE_LOAD_FAILED, {}

    if not isinstance(payload, dict):
        return ResultCode.TOOL_FILE_LOAD_FAILED, {}

    url = get_create_cart_url()
    headers = get_headers()
    headers["Authorization"] = f"Bearer {token}"

    status_code, response = post_and_parse_json(url, payload, headers=headers)

    if status_code >= 500:
        return ResultCode.SERVER_ERROR, {}

    if status_code != 200:
        return ResultCode.REQUESTS_EXCEPTION, {}

    return ResultCode.SUCCESS, response
