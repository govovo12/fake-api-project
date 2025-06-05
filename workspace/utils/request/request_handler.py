import requests
from typing import Any, Dict, Optional

def tool(func):
    """自製工具標記（供自動掃描工具表用）"""
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
    [TOOL] 最純粹 GET 請求，僅組裝並發送，SRP 單一責任原則。
    - 不負責 log、retry、副作用等行為
    - 其餘控制請於呼叫端加 decorator 或外部 controller
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
    [TOOL] 最純粹 POST 請求，僅組裝並發送，SRP 單一責任原則。
    - 不負責 log、retry、副作用等行為
    - 其餘控制請於呼叫端加 decorator 或外部 controller
    """
    return requests.post(url, headers=headers, json=json, timeout=timeout, **kwargs)
@tool
def post_json(
    url: str,
    payload: Dict[str, Any],
    headers: Optional[Dict[str, str]] = None,
    timeout: int = DEFAULT_TIMEOUT,
    **kwargs
) -> tuple:
    """
    [TOOL] 發送 POST 請求並嘗試解析 JSON 結果
    - 回傳 (code, dict)：成功回傳 200，其餘回傳錯誤碼與訊息
    - 若 API 無回應或格式錯誤，會有 fallback 保護
    """
    try:
        response = post(url, headers=headers, json=payload, timeout=timeout, **kwargs)
        if response.status_code == 200:
            return 200, response.json()
        else:
            return response.status_code, {"msg": f"API 回應非 200：{response.status_code}"}
    except Exception as e:
        return 500, {"msg": f"POST 請求失敗：{str(e)}"}
