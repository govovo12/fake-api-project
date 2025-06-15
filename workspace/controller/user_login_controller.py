from typing import Tuple, Optional
from workspace.modules.login.login_user import login_user
from workspace.utils.logger.log_helper import log_simple_result
from workspace.config.rules.error_codes import ResultCode
from workspace.utils.retry.retry_handler import retry_on_code


def login_and_report(cred: dict, headers: dict) -> Tuple[int, Optional[str]]:
    """
    子控制器：登入任務，含 retry 控制與錯誤碼 log
    """
    login_user_with_retry = retry_on_code(
        lambda c: login_user(c, headers),  # 封裝 headers
        retry_codes=[ResultCode.LOGIN_EXCEPTION],
        max_retries=3,
        delay=0.1
    )

    code, token = login_user_with_retry(cred)
    log_simple_result(code)
    return code, token
