import requests
from typing import Any, Dict, Optional, Tuple

def tool(func):
    """自製工具標記（供工具掃描）"""
    func.is_tool = True
    return func

DEFAULT_TIMEOUT = 5  # seconds

@tool
def get(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = DEFAULT_TIMEOUT,
    **kwargs
) -> requests.Response:
    """
    發送 GET 請求（純粹工具，不做錯誤處理與 log）
    """
    return requests.get(url, headers=headers, params=params, timeout=timeout, **kwargs)

@tool
def post(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    json: Optional[Dict[str, Any]] = None,
    timeout: int = DEFAULT_TIMEOUT,
    **kwargs
) -> requests.Response:
    """
    發送 POST 請求（純粹工具，不做錯誤處理與 log）
    """
    return requests.post(url, headers=headers, json=json, timeout=timeout, **kwargs)

@tool
def parse_json_safe(response: requests.Response) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    安全解析 JSON：成功回傳 (True, dict)，失敗回傳 (False, None)
    - 控制器可據此判斷是否進一步處理錯誤碼
    """
    try:
        return True, response.json()
    except Exception:
        return False, None

@tool
def post_and_parse_json(
    url: str,
    payload: Dict[str, Any],
    headers: Optional[Dict[str, str]] = None,
    timeout: int = DEFAULT_TIMEOUT,
    **kwargs
) -> Tuple[int, Optional[Dict[str, Any]]]:
    """
    發送 POST 並解析 JSON（不判斷成功與否、不印 log、不處理錯誤碼）
    - 回傳 (status_code, json 或 None)
    - 真正判斷邏輯由 controller 處理
    """
    response = post(url, headers=headers, json=payload, timeout=timeout, **kwargs)
    success, json_data = parse_json_safe(response)
    return response.status_code, json_data if success else None
