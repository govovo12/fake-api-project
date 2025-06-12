from typing import Optional
from workspace.config.rules.error_codes import ResultCode

# ✅ 工具標記（供 tools_table 掃描用）
def tool(func):
    """自製工具標記（供自動掃描工具表用）"""
    func.is_tool = True
    return func

# ✅ fallback 預設錯誤碼：當 APIError 沒指定錯誤碼時使用
DEFAULT_CODE = getattr(ResultCode, "GENERIC_ERROR", 9999)

# ✅ 允許的錯誤碼集合：幫助驗證傳入的錯誤碼是否合法
ALL_CODES = {
    v for k, v in vars(ResultCode).items()
    if not k.startswith("__") and isinstance(v, int)
}

# ✅ 自定義錯誤類別：用於 API 錯誤（含錯誤碼與 HTTP 狀態碼）
class APIError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None, code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code if code is not None else DEFAULT_CODE

        if self.code not in ALL_CODES:
            print(f"[警告] APIError 使用了未註冊的錯誤碼：{self.code}")

# ✅ 自定義錯誤類別：用於驗證錯誤（例如欄位格式不正確）
class ValidationError(Exception):
    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code

# ✅ 工具函式：處理任意例外並轉換為標準 dict 結構（供 controller log 或回應用）
@tool
def handle_exception(exc: Exception) -> dict:
    """
    [TOOL] 統一處理例外並轉換為 dict 格式
    - 支援 APIError（包含錯誤碼與 HTTP 狀態碼）
    - 支援 ValidationError（欄位驗證錯誤）
    - 其他錯誤會標示為 unknown
    """
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
