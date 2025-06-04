# tools: Response Helper 工具模組（Shopee 樣式）
# - 僅用 @tool 標記函式，不含 __task_info__
# - 提供任務模組用的 response 判斷與資料提取功能

from typing import Any, Optional


def tool(func):
    """自製工具標記（供工具表用）"""
    func.is_tool = True
    return func


@tool
def is_success(resp: dict) -> bool:
    """判斷是否為成功回應（code = 200 且含有 data 欄位）"""
    return resp.get("code") == 200 and "data" in resp


@tool
def extract_token(resp: dict) -> str:
    """從回應中提取 token 欄位"""
    return resp.get("data", {}).get("token", "")


@tool
def get_error_message(resp: dict) -> str:
    """從回應中提取錯誤訊息（優先使用 msg，其次 error）"""
    return resp.get("msg") or resp.get("error") or "未知錯誤"


@tool
def get_data_field(resp: dict, key: str) -> Optional[Any]:
    """從 data 欄位中提取指定欄位值"""
    return resp.get("data", {}).get(key)
