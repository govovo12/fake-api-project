# utils/uuid/uuid_generator.py

import uuid
from workspace.config.rules.error_codes import ResultCode

def tool(func):
    """工具模組標記裝飾器（供工具掃描器使用）"""
    func.is_tool = True
    return func

@tool
def generate_batch_uuid_with_code() -> tuple:
    """
    產生一組全域唯一的 UUID，標準回傳（error_code, uuid）
    """
    try:
        return ResultCode.SUCCESS, uuid.uuid4().hex
    except Exception:
        return ResultCode.UUID_GEN_FAIL, None
