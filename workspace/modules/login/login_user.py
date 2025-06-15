from typing import Tuple, Optional
from workspace.config.rules.error_codes import ResultCode
from workspace.config.paths import get_login_url
from workspace.utils.request.request_handler import post
from workspace.utils.response.response_helper import get_token_from_response


def login_user(cred: dict, headers: dict) -> Tuple[int, Optional[str]]:
    """
    登入任務：使用傳入帳密與 headers 進行 POST 請求，並擷取 token
    """
    try:
        response = post(get_login_url(), headers=headers, json=cred)
    except Exception:
        return ResultCode.LOGIN_EXCEPTION, None

    if response.status_code == 200:
        token = get_token_from_response(response)
        if token:
            return ResultCode.LOGIN_TASK_SUCCESS, token
        return ResultCode.LOGIN_API_FAILED, None
    else:
        return ResultCode.LOGIN_API_FAILED, None
