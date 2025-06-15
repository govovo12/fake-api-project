import requests
from typing import Optional, Tuple, Any
from workspace.utils.logger.trace_helper import print_trace
from workspace.config.rules.error_codes import ResultCode

# ✅ 自製工具標記
def tool(func):
    """自製工具標記（供工具表用）"""
    func.is_tool = True
    return func

@tool
def get(url: str, headers: Optional[dict] = None, params: Optional[dict] = None) -> requests.Response:
    """發送 GET 請求"""
    try:
        print_trace(f"GET 請求送出：url={url}")
        return requests.get(url, headers=headers, params=params, timeout=5)
    except Exception as e:
        print_trace(f"GET 發送失敗：{e}")
        raise

@tool
def post(url: str, headers: dict, json: Optional[dict] = None) -> requests.Response:
    """發送 POST 請求"""
    try:
        print_trace(f"POST 請求送出：url={url}")
        return requests.post(url, headers=headers, json=json, timeout=5)
    except Exception as e:
        print_trace(f"POST 發送失敗：{e}")
        raise

@tool
def parse_json_safe(response: requests.Response) -> Tuple[bool, Optional[dict]]:
    """嘗試解析 JSON，失敗時回 False, None"""
    try:
        return True, response.json()
    except Exception as e:
        print_trace(f"JSON 解析失敗：{e}")
        return False, None

@tool
def post_and_parse_json(url: str, payload: dict, headers: Optional[dict] = None) -> Tuple[int, Optional[Any]]:
    """POST 並解析 JSON，回傳 (status_code, json_data)"""
    response = post(url, headers=headers or {}, json=payload)
    success, data = parse_json_safe(response)
    return response.status_code, data
