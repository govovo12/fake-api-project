from typing import Dict

def tool(func):
    """自製工具標記（供自動掃描工具表用）"""
    func.is_tool = True
    return func

@tool
def enrich_with_uuid(data: Dict, uuid: str) -> Dict:
    """
    [TOOL] 將 dict 加工，附上 uuid 欄位，回傳新 dict（不修改原資料）
    
    Args:
        data (Dict): 原始資料
        uuid (str): 要加上的 UUID
    
    Returns:
        Dict: 帶 uuid 的新 dict

    範例：
        data = {"name": "test"}
        enrich_with_uuid(data, "abc-123")
        # -> {"name": "test", "uuid": "abc-123"}
    """
    new_data = data.copy()
    new_data["uuid"] = uuid
    return new_data
