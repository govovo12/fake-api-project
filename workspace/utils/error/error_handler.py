from typing import Optional
from workspace.config.rules.error_codes import ResultCode

# ✅ 裝飾器定義，放在檔案最上方
def tool(func):
    func.is_tool = True
    return func

DEFAULT_CODE = getattr(ResultCode, "GENERIC_ERROR", 9999)

ALL_CODES = {
    v for k, v in vars(ResultCode).items()
    if not k.startswith("__") and isinstance(v, int)
}


class APIError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None, code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code if code is not None else DEFAULT_CODE
        if self.code not in ALL_CODES:
            print(f"[警告] APIError 使用了未註冊的錯誤碼：{self.code}")


class ValidationError(Exception):
    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code


@tool  # ✅ 正確加上工具標記
def handle_exception(exc: Exception) -> dict:
    if isinstance(exc, APIError):
        return {
            "type": "api",
            "msg": str(exc),
            "code": exc.code,
            "status_code": exc.status_code,
        }
    elif isinstance(exc, ValidationError):
        return {
            "type": "validation",
            "msg": str(exc),
            "code": exc.code,
        }
    else:
        return {
            "type": "unknown",
            "msg": str(exc),
        }
