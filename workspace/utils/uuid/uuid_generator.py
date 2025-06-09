from typing import Tuple, Optional
import uuid
from workspace.config.rules.error_codes import ResultCode

def tool(func):
    func.is_tool = True
    return func

@tool
def generate_batch_uuid_with_code() -> Tuple[bool, Optional[str], Optional[dict]]:
    """
    工具模組：產生 UUID，回傳格式為 (success, uuid, meta)
    - 成功：True, uuid 字串, None
    - 失敗：False, None, meta（包含 code 與 message）
    """
    try:
        generated_uuid = uuid.uuid4().hex
        return True, generated_uuid, None
    except Exception as e:
        return False, None, {
            "code": ResultCode.UUID_GEN_FAIL,
            "message": str(e)
        }
def generate_uuid() -> str:
    """
    簡單版，直接產生並回傳 UUID 字串（不帶狀態）
    """
    import uuid
    return uuid.uuid4().hex
