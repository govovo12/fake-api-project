import json
from pathlib import Path
from workspace.utils.file.file_helper import save_json

# ✅ 工具函式標記（供 tools_table 掃描用）
def tool(func):
    func.is_tool = True
    return func

@tool
def write_empty_data_file(path: Path, kind: str):
    """
    建立指定種類（使用者/商品）的空白 JSON 檔案。

    Args:
        path (Path): 欲寫入的檔案路徑。
        kind (str): 資料種類，例如 'user' 或 'product'。

    Returns:
        Tuple[bool, Optional[dict]]:
        - 成功時回傳 (True, {})
        - 失敗時回傳 (False, meta)，其中 meta 包含 reason, message, path, kind 等錯誤資訊。
    """
    try:
        result = save_json(path, {})
        if not result:
            return False, {
                "reason": f"save_failed_{kind}",
                "message": "save_json returned False",
                "path": str(path),
                "kind": kind
            }
        return True, {}
    except Exception as e:
        return False, {
            "reason": f"save_failed_{kind}",
            "message": str(e),
            "path": str(path),
            "kind": kind
        }
@tool
def generate_empty_data(kind: str) -> dict:
    """
    根據種類產生對應的空白資料結構。

    Args:
        kind (str): 'user' 或 'product'

    Returns:
        dict: 對應空資料，未知種類則回傳空 dict
    """
    if kind == "user":
        return {
            "uuid": "",
            "name": "",
            "email": ""
        }
    elif kind == "product":
        return {
            "uuid": "",
            "name": "",
            "price": 0
        }
    return {}
