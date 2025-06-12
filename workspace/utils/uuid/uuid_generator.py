from workspace.config.rules.error_codes import ResultCode
import uuid

def generate_batch_uuid_with_code() -> str:
    """
    工具模組：產生一筆 UUID 字串。
    - 成功：回傳 UUID
    - 失敗：回傳錯誤碼（int）
    """
    try:
        return uuid.uuid4().hex
    except Exception:
        return ResultCode.UUID_GEN_FAIL
