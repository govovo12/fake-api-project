from typing import Any, Optional
import requests
from workspace.config.rules.error_codes import ResultCode

def tool(func):
    """自製工具標記（供工具表用）"""
    func.is_tool = True
    return func

# ✅ dict 類型 response 工具

@tool
def get_code_from_dict(resp: dict) -> Optional[int]:
    """取得 code 欄位（若不存在則回傳 None）"""
    return resp.get("code")

@tool
def get_data_field_from_dict(resp: dict, key: str) -> Optional[Any]:
    """從 data 區塊中提取指定欄位值"""
    return resp.get("data", {}).get(key)

@tool
def get_token_from_dict(resp: dict) -> Optional[str]:
    """從 data 區塊中提取 token"""
    return resp.get("data", {}).get("token")

@tool
def get_error_message_from_dict(resp: dict) -> str:
    """優先從 msg，其次 error 擷取錯誤訊息"""
    return resp.get("msg") or resp.get("error") or "未知錯誤"


# ✅ requests.Response 類型 response 工具

@tool
def get_status_code_from_response(response: requests.Response) -> int:
    """取得 HTTP status code"""
    return response.status_code

@tool
def get_json_field_from_response(response: requests.Response, field: str) -> Optional[Any]:
    """從 JSON 中擷取指定欄位值，若解析失敗回 None"""
    try:
        return response.json().get(field)
    except Exception:
        return None  # ⚠️ 

@tool
def get_data_field_from_response(response: requests.Response, key: str) -> Optional[Any]:
    """從 JSON 的 data 區塊中擷取指定欄位，若解析失敗回 None"""
    try:
        return response.json().get("data", {}).get(key)
    except Exception:
        return None

@tool
def get_token_from_response(response: requests.Response) -> Optional[str]:
    """擷取 JSON 的 data.token 欄位，若解析失敗回 None"""
    try:
        return response.json().get("data", {}).get("token")
    except Exception:
        return None

@tool
def get_error_message_from_response(response: requests.Response) -> str:
    """擷取 msg 或 error 為錯誤訊息，若解析失敗回 '回傳格式錯誤'"""
    try:
        json_data = response.json()
        return json_data.get("msg") or json_data.get("error") or "未知錯誤"
    except Exception:
        return "回傳格式錯誤"
