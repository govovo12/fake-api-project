from typing import Dict
from workspace.config.rules.error_codes import ResultCode, TaskModuleError

# ✅ 工具函式標記（供 tools_table 掃描用）
def tool(func):
    func.is_tool = True
    return func


@tool
def enrich_with_uuid(data: dict, uuid: str) -> dict:
    """
    加上 uuid 欄位，回傳新資料（不修改原 dict）。
    僅檢查資料型別與 clone 操作，不處理 uuid 的業務邏輯。
    """
    if not isinstance(data, dict):
        raise TaskModuleError(ResultCode.NOT_A_DICT)

    try:
        new_data = data.copy()
        new_data["uuid"] = uuid  # ✅ 無論 uuid 是否為空，都原樣加上
        return new_data
    except Exception:
        raise TaskModuleError(ResultCode.ENRICH_WITH_UUID_FAILED)


@tool
def enrich_payload(data: dict, fields_str: str) -> Dict[str, object]:
    """
    根據 .env 的欄位設定（逗號分隔）從資料中取值並組裝 payload。
    """
    try:
        keys = [key.strip() for key in fields_str.split(",") if key.strip()]
        return {key: data.get(key) for key in keys}
    except Exception:
        raise TaskModuleError(ResultCode.ENRICH_PAYLOAD_FAILED)
