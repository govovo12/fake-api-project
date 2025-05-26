# workspace/modules/login/login_token_writer.py

from .login_schema import LoginResult
from config.rules import runtime_vars


def store_token(result: LoginResult) -> None:
    """
    將成功登入的 token 儲存至全域 runtime_vars 中
    """
    if result.success and result.token:
        runtime_vars.jwt_token = result.token
