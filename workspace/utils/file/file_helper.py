from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

# ✅ 自製工具標記器
def tool(func):
    """自製工具標記（供工具掃描器使用）"""
    func.is_tool = True
    return func

# ✅ 檔案與資料夾處理工具

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
def is_file_empty(path: Path) -> bool:
    """[TOOL] 判斷指定檔案是否為空。"""
    return path.is_file() and path.stat().st_size == 0

@tool
def get_file_name_from_path(path: Path) -> str:
    """[TOOL] 取得檔案名稱（含副檔名）。"""
    return path.name

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

# ✅ JSON 檔案通用工具

@tool
def load_json(path: Path, encoding: str = "utf-8") -> Optional[dict]:
    """[TOOL] 載入 JSON 檔案內容，失敗回傳 None。"""
    try:
        import json
        with path.open("r", encoding=encoding) as f:
            return json.load(f)
    except Exception:
        return None

@tool
def save_json(data: dict, path: Path, indent: int = 2, encoding: str = "utf-8") -> bool:
    """[TOOL] 安全儲存 JSON。成功回傳 True，失敗 False。使用臨時檔確保原檔不被破壞。"""
    try:
        import json
        from tempfile import NamedTemporaryFile

        # 確保目錄存在
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)

        # 寫入暫存檔
        with NamedTemporaryFile("w", delete=False, suffix=".tmp", dir=path.parent, encoding=encoding) as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=indent)
            tmp_path = Path(tmp.name)

        # 成功後搬正
        tmp_path.replace(path)
        return True
    except Exception:
        return False

