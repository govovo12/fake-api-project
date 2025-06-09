from typing import Dict, Tuple, Optional

# ✅ 工具函式標記（供 tools_table 掃描用）
def tool(func):
    func.is_tool = True
    return func


@tool
def enrich_with_uuid(data: dict, uuid: str) -> Tuple[bool, Optional[dict], Optional[dict]]:
    """
    加上 uuid 欄位，回傳新資料（不修改原 dict）。
    僅檢查資料型別與 clone 操作，不處理 uuid 的業務邏輯。
    """
    if not isinstance(data, dict):
        return False, None, {
            "reason": "not_a_dict",
            "message": "傳入參數 data 不是 dict 類型",
        }

    try:
        new_data = data.copy()
        new_data["uuid"] = uuid  # ✅ 無論 uuid 是否為空，都原樣加上
        return True, new_data, None
    except Exception as e:
        return False, None, {
            "reason": "enrich_failed",
            "message": str(e)
        }


@tool
def enrich_payload(data: dict, fields_str: str) -> dict:
    """
    根據 .env 的欄位設定（逗號分隔）從資料中取值並組裝 payload。
    """
    keys = [key.strip() for key in fields_str.split(",") if key.strip()]
    return {key: data.get(key) for key in keys}