from typing import Tuple, Optional

# -----------------------------
# 🧪 任務模組
# -----------------------------
from workspace.modules.login.login_user import login_user

# -----------------------------
# 🧰 工具與設定
# -----------------------------
from workspace.utils.logger.log_helper import log_simple_result
from workspace.config.rules.error_codes import ResultCode
from workspace.utils.retry.retry_handler import retry_on_code


def login_and_report(cred: dict, headers: dict) -> Tuple[int, Optional[str]]:
    """
    子控制器：登入任務，負責處理 retry 機制與統一印出。
    """
    def wrapped_login(c):
        return login_user(c, headers)

    login_user_with_retry = retry_on_code(
        wrapped_login,
        retry_codes=[ResultCode.LOGIN_EXCEPTION],
        max_retries=3,
        delay=0.1
    )

    code, token = login_user_with_retry(cred)

    if code != ResultCode.SUCCESS:
        log_simple_result(code)
        return code, token

    log_simple_result(ResultCode.LOGIN_TASK_SUCCESS)
    return ResultCode.LOGIN_TASK_SUCCESS, token
