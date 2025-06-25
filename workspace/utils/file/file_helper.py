import json
from pathlib import Path
from workspace.config.rules.error_codes import ResultCode


# ✅ tools 裝飾器
def tool(func):
    func.is_tool = True
    return func


@tool
def ensure_dir(path: Path) -> int:
    """
    若目錄不存在則建立，並回傳成功或錯誤碼。
    """
    if not isinstance(path, Path):
        return ResultCode.TOOL_INVALID_FILE_DATA
    try:
        path.mkdir(parents=True, exist_ok=True)
        return ResultCode.SUCCESS
    except Exception:
        return ResultCode.TOOL_DIR_CREATE_FAILED


@tool
def ensure_file(path: Path) -> int:
    """
    若檔案不存在則建立空檔案，並回傳成功或錯誤碼。
    """
    if not isinstance(path, Path):
        return ResultCode.TOOL_INVALID_FILE_DATA
    try:
        if not path.exists():
            result = ensure_dir(path.parent)
            if result != ResultCode.SUCCESS:
                return result
            path.touch()
        return ResultCode.SUCCESS
    except Exception:
        return ResultCode.TOOL_FILE_CREATE_FAILED


@tool
def file_exists(path: Path) -> bool:
    """
    檢查檔案是否存在。
    """
    if not isinstance(path, Path):
        return False
    return path.is_file()


@tool
def is_file_empty(path: Path):
    """
    檢查檔案是否為空（0 bytes），正常回傳 bool，失敗回傳錯誤碼。
    """
    if not isinstance(path, Path):
        return ResultCode.TOOL_INVALID_FILE_DATA
    try:
        return path.stat().st_size == 0
    except Exception:
        return ResultCode.TOOL_FILE_STAT_FAILED


@tool
def clear_file(path: Path) -> int:
    """
    清空檔案內容（不刪檔）並回傳成功或錯誤碼。
    """
    if not isinstance(path, Path):
        return ResultCode.TOOL_INVALID_FILE_DATA
    try:
        if path.exists():
            path.write_text("", encoding="utf-8")
        return ResultCode.SUCCESS
    except Exception:
        return ResultCode.TOOL_FILE_CLEAR_FAILED


@tool
def delete_file(path: Path) -> int:
    """
    刪除指定檔案，若不存在則視為成功。
    """
    if not isinstance(path, Path):
        return ResultCode.TOOL_INVALID_FILE_DATA
    try:
        if path.exists():
            path.unlink()
        return ResultCode.SUCCESS
    except Exception:
        return ResultCode.TOOL_FILE_DELETE_FAILED



