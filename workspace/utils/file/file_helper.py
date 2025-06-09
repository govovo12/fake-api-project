import json
from pathlib import Path
from typing import Optional, Tuple
from workspace.config.rules.error_codes import ResultCode

def tool(func):
    func.is_tool = True
    return func

@tool
def ensure_dir(path: Path) -> None:
    """
    若目錄不存在則建立
    """
    path.mkdir(parents=True, exist_ok=True)

@tool
def ensure_file(path: Path) -> None:
    """
    若檔案不存在則建立空檔案
    """
    if not path.exists():
        ensure_dir(path.parent)
        path.touch()

@tool
def file_exists(path: Path) -> bool:
    """
    檢查檔案是否存在
    """
    return path.is_file()

@tool
def is_file_empty(path: Path) -> bool:
    """
    檢查檔案是否為空（0 bytes）
    """
    return path.stat().st_size == 0

@tool
def get_file_name_from_path(path: Path) -> str:
    """
    從 Path 回傳檔名
    """
    return path.name

@tool
def clear_file(path: Path) -> None:
    """
    清空檔案內容（不刪檔）
    """
    if path.exists():
        path.write_text("", encoding="utf-8")

@tool
def save_json(path: Path, data: dict) -> Tuple[bool, Optional[dict]]:
    """
    儲存 JSON 至指定路徑
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True, None
    except TypeError as e:
        return False, {
            "code": ResultCode.FILE_SERIALIZATION_FAILED,
            "message": str(e),
            "path": str(path),
        }
    except Exception as e:
        return False, {
            "code": ResultCode.FILE_WRITE_FAILED,
            "message": str(e),
            "path": str(path),
        }

@tool
def generate_testdata_path(kind: str, uuid: str) -> Tuple[Optional[Path], Optional[dict]]:
    """
    回傳測資儲存路徑。若格式不合法，回傳錯誤。
    kind: user / product
    """
    if kind not in {"user", "product"}:
        return None, {
            "code": ResultCode.INVALID_FILE_KIND,
            "message": f"無效資料類型: {kind}",
            "kind": kind
        }

    if not isinstance(uuid, str) or not uuid or len(uuid.replace("-", "")) != 32:
        return None, {
            "code": ResultCode.UUID_FORMAT_INVALID,
            "message": f"無效 UUID 格式: {uuid}",
            "uuid": uuid
        }

    path = Path(f"workspace/testdata/{kind}/{uuid}.json")
    return path, None

import uuid

@tool
def write_temp_file(data: str, suffix=".tmp") -> Path:
    """
    將資料寫入暫存檔並回傳路徑
    """
    temp_path = Path(f"workspace/.tmp/{uuid.uuid4().hex}{suffix}")
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path.write_text(data, encoding="utf-8")
    return temp_path
