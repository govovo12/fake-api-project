from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

def tool(func):
    """自製工具標記（供自動掃描工具表用）"""
    func.is_tool = True
    return func

@tool
def ensure_dir(path: Path) -> None:
    """[TOOL] 確保資料夾存在，若不存在則建立。"""
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

@tool
def ensure_file(path: Path) -> None:
    """[TOOL] 確保檔案存在，若上層資料夾不存在則一併建立。"""
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()

@tool
def file_exists(path: Path) -> bool:
    """[TOOL] 檢查檔案是否存在。"""
    return path.is_file()

@tool
def get_file_name_from_path(path: Path) -> str:
    """[TOOL] 取得檔案名稱（含副檔名）。"""
    return path.name

@tool
def is_file_empty(path: Path) -> bool:
    """[TOOL] 判斷指定檔案是否為空。"""
    return path.is_file() and path.stat().st_size == 0

@tool
def clear_file(path: Path) -> None:
    """[TOOL] 清空指定檔案內容，若不存在則略過。"""
    if path.is_file():
        path.write_text("", encoding="utf-8")

@tool
def write_temp_file(content: str, suffix: str = ".txt") -> Path:
    """[TOOL] 寫入暫存檔案，回傳檔案路徑。"""
    with NamedTemporaryFile(delete=False, mode="w", suffix=suffix, encoding="utf-8") as f:
        f.write(content)
        return Path(f.name)
@tool
def clear_dir_files(target_dir: Path, suffix: str = ".json") -> int:
    """[TOOL] 批次刪除指定資料夾下所有指定副檔名的檔案。
    Args:
        target_dir (Path): 目標資料夾路徑
        suffix (str): 指定副檔名，預設 ".json"
    Returns:
        int: 成功刪除的檔案數量
    """
    count = 0
    if target_dir.exists():
        for f in target_dir.iterdir():
            if f.is_file() and f.name.endswith(suffix):
                f.unlink()
                count += 1
    return count

@tool
def read_json(path: Path, encoding: str = "utf-8") -> Optional[dict]:
    """[TOOL] 讀取 JSON 檔案內容，若失敗則回傳 None。"""
    try:
        import json
        with path.open("r", encoding=encoding) as f:
            return json.load(f)
    except Exception:
        return None
@tool
def save_json(data: dict, path: Path, indent: int = 2, encoding: str = "utf-8") -> bool:
    """[TOOL] 儲存 JSON 至指定路徑。成功回傳 True，失敗 False。"""
    try:
        import json
        with path.open("w", encoding=encoding) as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        return True
    except Exception:
        return False
@tool
def load_json(path: Path, encoding: str = "utf-8") -> Optional[dict]:
    """[TOOL] 載入 JSON 檔案內容，失敗回傳 None。"""
    try:
        import json
        with path.open("r", encoding=encoding) as f:
            return json.load(f)
    except Exception:
        return None
