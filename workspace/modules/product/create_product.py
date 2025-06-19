"""
建立商品任務模組：讀取測資檔並呼叫 API 建立商品
"""

from workspace.utils.data.data_loader import load_json
from workspace.config.paths import get_product_path, get_create_product_url, get_headers
from workspace.utils.request.request_handler import post_and_parse_json
from workspace.config.rules.error_codes import ResultCode


def create_product(uuid: str, token: str = "") -> tuple[int, dict | None]:
    """
    根據指定 UUID 讀取測資檔案，發送建立商品 API 請求。

    Args:
        uuid (str): 商品測資檔案的 UUID（對應測資 JSON 檔）
        token (str): 可選的 Bearer token（預設為空，Fake Store API 不驗證）

    Returns:
        tuple[int, dict | None]: (ResultCode, 回傳資料或 None)
    """

    # 讀取商品測資檔案
    path = get_product_path(uuid)
    payload = load_json(path)

    if not isinstance(payload, dict):
        return ResultCode.TOOL_FILE_LOAD_FAILED, None

    url = get_create_product_url()
    headers = get_headers()

    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        status_code, response = post_and_parse_json(url, payload, headers)
    except Exception:
        return ResultCode.REQUESTS_EXCEPTION, None

    if status_code == 200:
        return ResultCode.CREATE_PRODUCT_SUCCESS, response
    elif 500 <= status_code < 600:
        return ResultCode.SERVER_ERROR, response
    else:
        return ResultCode.CREATE_PRODUCT_FAILED, response
