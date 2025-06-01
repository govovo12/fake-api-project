from workspace.config.rules import error_codes
from typing import Any, Dict, Optional, Callable

def tool(func):
    """自製工具標記（供自動掃描工具表用）"""
    func.is_tool = True
    return func

class APIError(Exception):
    """[TOOL] API 相關自定義錯誤，可攜帶 status_code 與 code。"""
    def __init__(self, message: str, status_code: Optional[int] = None, code: int = error_codes.API_TIMEOUT):
        super().__init__(message)
        self.status_code = status_code
        self.code = code

class ValidationError(Exception):
    """[TOOL] 資料驗證相關錯誤，可攜帶 code 字串。"""
    def __init__(self, message: str, code: str = "VALIDATION_ERROR"):
        super().__init__(message)
        self.code = code

@tool
def handle_exception(
    e: Exception,
    log: Optional[Callable[[str], None]] = None
) -> Dict[str, Any]:
    """
    [TOOL] 統一將 Exception 轉為標準 dict，可選擇傳入 log callback。
    - 支援 APIError/ValidationError，其他視為 unknown
    - log: 可傳入 callable（msg: str），遇錯誤時可記錄（非必要）
    """
    if isinstance(e, APIError):
        if log:
            log(f"[APIError] code={e.code}, status_code={e.status_code}, msg={str(e)}")
        return {
            "type": "api",
            "code": e.code,
            "status_code": e.status_code,
            "msg": str(e),
        }
    elif isinstance(e, ValidationError):
        if log:
            log(f"[ValidationError] code={e.code}, msg={str(e)}")
        return {
            "type": "validation",
            "code": e.code,
            "msg": str(e),
        }
    else:
        if log:
            log(f"[UnknownError] msg={str(e)}")
        return {
            "type": "unknown",
            "msg": str(e),
        }
