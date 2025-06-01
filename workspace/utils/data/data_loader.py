import json
from pathlib import Path
from typing import Callable, Optional, Dict, Any, List, Union

def tool(func):
    """自製工具標記（供自動掃描工具表用）"""
    func.is_tool = True
    return func

@tool
def load_json(
    path: Path,
    encoding: str = "utf-8",
    on_error: Optional[Callable[[Exception, Path], None]] = None
) -> Dict[str, Any]:
    """
    [TOOL] 嘗試讀取 JSON 檔案並回傳 dict。
    - path: JSON 檔案路徑
    - encoding: 檔案編碼，預設 utf-8
    - on_error: 例外處理 callback，可自訂 log 行為。型態 (Exception, Path) -> None

    失敗時會回傳空 dict，並可選擇執行 on_error。
    """
    try:
        with open(path, encoding=encoding) as f:
            return json.load(f)
    except Exception as e:
        if on_error:
            on_error(e, path)
        return {}

@tool
def save_json(
    data: Dict[str, Any],
    path: Path,
    encoding: str = "utf-8",
    indent: int = 2,
    on_error: Optional[Callable[[Exception, Path], None]] = None
) -> bool:
    """
    [TOOL] 將 dict 儲存成 JSON 檔案，成功回傳 True，失敗回傳 False。
    """
    try:
        with open(path, "w", encoding=encoding) as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        return True
    except Exception as e:
        if on_error:
            on_error(e, path)
        return False

@tool
def load_jsons(
    folder: Path,
    encoding: str = "utf-8",
    on_error: Optional[Callable[[Exception, Path], None]] = None
) -> Dict[str, Dict[str, Any]]:
    """
    [TOOL] 批次讀取資料夾下所有 json 檔，回傳 {檔名: dict}
    """
    result = {}
    for f in folder.glob("*.json"):
        result[f.name] = load_json(f, encoding=encoding, on_error=on_error)
    return result
