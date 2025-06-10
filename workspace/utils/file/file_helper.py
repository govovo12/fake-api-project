import json
import uuid
from pathlib import Path
from typing import Optional

from workspace.config.rules.error_codes import ResultCode

# ✅ 自定義錯誤（可搬至 exceptions.py）
class TaskModuleError(Exception):
    def __init__(self, code: int):
        self.code = code
        super().__init__(f"[{code}]")


# ✅ tools 裝飾器
def tool(func):
    func.is_tool = True
    return func


@tool
def ensure_dir(path: Path) -> None:
    """
    若目錄不存在則建立
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception:
        raise TaskModuleError(ResultCode.DIR_CREATE_FAILED)


@tool
def ensure_file(path: Path) -> None:
    """
    若檔案不存在則建立空檔案
    """
    try:
        if not path.exists():
            ensure_dir(path.parent)
            path.touch()
    except Exception:
        raise TaskModuleError(ResultCode.FILE_CREATE_FAILED)


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
    try:
        return path.stat().st_size == 0
    except Exception:
        raise TaskModuleError(ResultCode.FILE_STAT_FAILED)


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
    try:
        if path.exists():
            path.write_text("", encoding="utf-8")
    except Exception:
        raise TaskModuleError(ResultCode.FILE_CLEAR_FAILED)


@tool
def save_json(path: Path, data: dict) -> None:
    """
    儲存 JSON 至指定路徑
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except TypeError:
        raise TaskModuleError(ResultCode.FILE_SERIALIZATION_FAILED)
    except Exception:
        raise TaskModuleError(ResultCode.FILE_WRITE_FAILED)


@tool
def generate_testdata_path(kind: str, uuid_str: str) -> Path:
    """
    回傳測資儲存路徑。若格式不合法，拋出錯誤。
    kind: user / product
    """
    if kind not in {"user", "product"}:
        raise TaskModuleError(ResultCode.INVALID_FILE_KIND)

    if not isinstance(uuid_str, str) or not uuid_str or len(uuid_str.replace("-", "")) != 32:
        raise TaskModuleError(ResultCode.UUID_FORMAT_INVALID)

    return Path(f"workspace/testdata/{kind}/{uuid_str}.json")


@tool
def write_temp_file(data: str, suffix: str = ".tmp") -> Path:
    """
    將資料寫入暫存檔並回傳路徑
    """
    try:
        temp_path = Path(f"workspace/.tmp/{uuid.uuid4().hex}{suffix}")
        temp_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path.write_text(data, encoding="utf-8")
        return temp_path
    except Exception:
        raise TaskModuleError(ResultCode.TEMP_FILE_WRITE_FAILED)
