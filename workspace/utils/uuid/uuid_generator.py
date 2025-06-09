from typing import Tuple, Optional
import uuid

# ✅ 自製工具函式標記（供 tools_table 掃描用）
def tool(func):
    func.is_tool = True
    return func

@tool
def generate_batch_uuid_with_code() -> Tuple[bool, Optional[str], Optional[dict]]:
    """
    工具模組：產生 UUID，回傳格式為 (success, uuid, meta)
    - 成功：True, uuid 字串, None
    - 失敗：False, None, meta（包含 reason 與 message）
    """
    try:
        generated_uuid = uuid.uuid4().hex
        return True, generated_uuid, None
    except Exception as e:
        return False, None, {
            "reason": "uuid_generate_failed",
            "message": str(e)
        }
