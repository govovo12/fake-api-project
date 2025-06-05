from typing import Any, Optional
import requests


def tool(func):
    """自製工具標記（供工具表用）"""
    func.is_tool = True
    return func


# ✅ dict 類型 response（多用於 mock 或已轉換的 API 回應）
@tool
def is_success_dict(resp: dict) -> bool:
    """判斷是否為成功回應（code = 200 且含有 data 欄位）"""
    return resp.get("code") == 200 and "data" in resp


@tool
def extract_token_from_dict(resp: dict) -> str:
    """從 dict response 中提取 token 欄位"""
    return resp.get("data", {}).get("token", "")


@tool
def get_error_message_from_dict(resp: dict) -> str:
    """從 dict response 中提取錯誤訊息（優先 msg，其次 error）"""
    return resp.get("msg") or resp.get("error") or "未知錯誤"


@tool
def get_data_field_from_dict(resp: dict, key: str) -> Optional[Any]:
    """從 dict response 的 data 欄位中提取指定欄位值"""
    return resp.get("data", {}).get(key)


@tool
def is_register_success_dict(resp: dict) -> bool:
    """判斷註冊是否成功（dict response 中有 id）"""
    return isinstance(resp, dict) and "id" in resp


# ✅ requests.Response 類型 response（直接來自 requests 回傳）
@tool
def get_json_field_from_response(response: requests.Response, field: str) -> Optional[Any]:
    """從 requests.Response 物件的 JSON 中擷取指定欄位，失敗回傳 None"""
    try:
        return response.json().get(field)
    except Exception:
        return None


@tool
def get_data_field_from_response(response: requests.Response, field: str) -> Optional[Any]:
    """從 requests.Response 的 JSON → data 區段中提取欄位"""
    try:
        return response.json().get("data", {}).get(field)
    except Exception:
        return None


@tool
def is_status_code_success(response: requests.Response) -> bool:
    """判斷 requests.Response 狀態碼是否為 200"""
    return response.status_code == 200
@tool
def get_error_message_dict(resp: dict) -> str:
    """從 dict response 中提取錯誤訊息（優先使用 msg，其次 error）"""
    return resp.get("msg") or resp.get("error") or "未知錯誤"
@tool
def extract_token_dict(resp: dict) -> str:
    """從 dict response 中提取 token"""
    return resp.get("data", {}).get("token", "")
