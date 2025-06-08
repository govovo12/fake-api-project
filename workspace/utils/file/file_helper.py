from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Tuple, Optional, Dict, List, Union
import json

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
    """
    若檔案存在則刪除，不 raise error。
    """
    try:
        if path.exists():
            path.unlink()
    except Exception:
        pass  

@tool
def write_temp_file(prefix: str, content: str = "") -> Path:
    """
    建立一個暫存檔案，寫入指定內容。
    """
    import tempfile

    tmp = Path(tempfile.mktemp(prefix=f"{prefix}_", suffix=".tmp"))
    tmp.write_text(content, encoding="utf-8")
    return tmp


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
def save_json(path: Path, data: dict) -> Tuple[bool, Optional[dict]]:
    """
    將 dict 寫入 JSON 檔案，支援錯誤通報。
    """
    try:
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
    except TypeError as e:
        return False, {
            "reason": "json_serialization_failed",
            "message": str(e),
            "path": str(path)
        }
    try:
        path.write_text(json_str, encoding="utf-8")
        return True, None
    except Exception as e:
        return False, {
            "reason": "save_failed",
            "message": str(e),
            "path": str(path)
        }


@tool
def get_testdata_file_path(kind: str, uuid: str) -> Tuple[bool, Optional[Path], Optional[dict]]:
    """
    組合測試資料儲存用的路徑，格式為：.generated/{kind}/{uuid}.json

    Args:
        kind (str): 資料種類（例如 user, product）
        uuid (str): UUID 或識別字串

    Returns:
        Tuple: (success, path 或 None, meta 或 None)
    """
    VALID_KINDS = {"user", "product", "order"}

    if kind not in VALID_KINDS:
        return False, None, {
            "reason": "invalid_kind",
            "message": f"無效類型：{kind}，必須是 {sorted(VALID_KINDS)}"
        }

    if not uuid or not isinstance(uuid, str):
        return False, None, {
            "reason": "invalid_uuid",
            "message": f"uuid 格式錯誤：{uuid}"
        }

    try:
        base_dir = Path("workspace/.generated") / kind
        base_dir.mkdir(parents=True, exist_ok=True)
        return True, base_dir / f"{uuid}.json", None
    except Exception as e:
        return False, None, {
            "reason": "path_generation_failed",
            "message": str(e),
            "context": {"kind": kind, "uuid": uuid}
        }

