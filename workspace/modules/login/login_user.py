# --------------------------
# 📦 錯誤碼與配置
# --------------------------
from typing import Tuple, Optional
from workspace.config.rules.error_codes import ResultCode
from workspace.config.paths import get_login_url

# --------------------------
# 🧰 工具模組
# --------------------------
from workspace.utils.request.request_handler import post
from workspace.utils.response.response_helper import get_token_from_response


def login_user(cred: dict, headers: dict) -> Tuple[int, Optional[str]]:
    """
    登入任務：使用傳入帳密與 headers 進行 POST 請求，並擷取 token。

    Args:
        cred (dict): 登入憑證，格式如 {"username": ..., "password": ...}
        headers (dict): HTTP headers，應包含 Content-Type 等資訊

    Returns:
        Tuple[int, Optional[str]]:
            - 成功：ResultCode.SUCCESS, token
            - 失敗：對應錯誤碼, None
    """
    try:
        response = post(get_login_url(), headers=headers, json=cred)
    except Exception:
        return ResultCode.LOGIN_EXCEPTION, None

    if response.status_code == 200:
        token = get_token_from_response(response)
        if token:
            return ResultCode.SUCCESS, token  

    return ResultCode.LOGIN_API_FAILED, None
