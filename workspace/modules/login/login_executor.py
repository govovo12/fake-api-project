from .login_worker import do_login
from .login_schema import LoginRequest, LoginResult
from config.rules.login_config import (
    LOGIN_RETRY_COUNT,
    LOGIN_RETRY_DELAY,
    LOGIN_RETRY_BACKOFF
)
from utils.retry_helper import retry_call



def execute_login(request: LoginRequest) -> LoginResult:
    """
    包裝 login_worker，加入 retry_call 機制，回傳 LoginResult 結構
    """
    return retry_call(
        func=do_login,
        max_retries=LOGIN_RETRY_COUNT,
        delay=LOGIN_RETRY_DELAY,
        backoff=LOGIN_RETRY_BACKOFF,
        exceptions=(Exception,),
        req=request
    )