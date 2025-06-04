# utils/uuid/uuid_generator.py

import uuid

# ✅ 標準工具函式裝飾器
def tool(func):
    """工具模組標記裝飾器（供工具掃描器使用）"""
    func.is_tool = True
    return func

@tool
def generate_batch_uuid() -> str:
    """
    產生一組全域唯一的 UUID（32 字元十六進位字串） [TOOL]

    用於標記單次測資批次、流程執行等識別用。
    """
    return uuid.uuid4().hex
