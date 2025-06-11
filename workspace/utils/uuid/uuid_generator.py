from typing import Optional
import uuid
from workspace.config.rules.error_codes import ResultCode

# ✅ 工具函式標記（供 tools_table 掃描用）
def tool(func):
    func.is_tool = True
    return func

@tool
def generate_batch_uuid_with_code() -> str:
    """
    工具模組：產生一組 UUID 字串。
    - 成功：回傳 UUID 字串
    - 失敗：回傳錯誤碼
    """
    try:
        return uuid.uuid4().hex  # 生成 UUID 並返回
    except Exception as e:
        # 如果出錯，回傳錯誤碼
        
        return ResultCode.UUID_GEN_FAIL  # 回傳錯誤碼


@tool
def generate_uuid() -> str:
    """
    工具模組：簡單產生單一 UUID 字串。
    - 成功：回傳 UUID 字串
    - 失敗：回傳錯誤碼
    """
    try:
        return uuid.uuid4().hex  # 生成 UUID 並返回
    except Exception as e:
        # 如果出錯，回傳錯誤碼
        
        return ResultCode.UUID_GEN_FAIL  # 回傳錯誤碼
