from workspace.config.rules.error_codes import ResultCode
from workspace.config.paths import get_user_path
from workspace.utils.data.data_loader import load_json
from workspace.utils.request.request_handler import post
from workspace.utils.response.response_helper import get_status_code_from_response


def register_user(uuid: str, url: str, headers: dict) -> int:
    """
    註冊 Fake Store API 使用者：
    - 從指定 uuid 取得測資 payload
    - 發送 POST 請求到指定 URL（含 headers）
    - 根據 response 回傳錯誤碼

    :param uuid: 測資識別碼（對應 user 測資檔案）
    :param url: API 註冊入口（例如 https://fakestoreapi.com/users）
    :param headers: 呼叫 API 所需的 headers
    :return: int 統一錯誤碼（成功為 0，錯誤為 ResultCode 內定義）
    """
    path = get_user_path(uuid)
    payload = load_json(path)

    if not isinstance(payload, dict):
        return payload  # 載入失敗會直接是錯誤碼 int

    try:
        response = post(url=url, headers=headers, json=payload)
        status = get_status_code_from_response(response)

        if status in (200, 201):
            return 0
        return ResultCode.FAKER_REGISTER_FAILED
    except Exception:
        return ResultCode.FAKER_REGISTER_EXCEPTION
