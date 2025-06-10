from typing import Optional
import uuid
from workspace.config.rules.error_codes import ResultCode
from workspace.config.rules.error_codes import TaskModuleError  # ✅ 使用統一錯誤類型

def tool(func):
    func.is_tool = True
    return func

@tool
def generate_batch_uuid_with_code() -> str:
    """
    工具模組：產生 UUID 字串。
    - 成功：回傳 UUID 字串
    - 失敗：拋出 TaskModuleError（含錯誤碼）
    """
    try:
        return uuid.uuid4().hex
    except Exception:
        raise TaskModuleError(ResultCode.UUID_GEN_FAIL)

@tool
def generate_uuid() -> str:
    """
    工具模組：簡單產生 UUID 字串。
    """
    return uuid.uuid4().hex
