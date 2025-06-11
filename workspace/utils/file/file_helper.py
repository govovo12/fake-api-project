import json
import uuid
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
    try:
        path.mkdir(parents=True, exist_ok=True)
        return ResultCode.SUCCESS  # 成功
    except Exception as e:
        
        return ResultCode.TOOL_DIR_CREATE_FAILED  # 目錄創建失敗


@tool
def ensure_file(path: Path) -> int:
    """
    若檔案不存在則建立空檔案，並回傳成功或錯誤碼。
    """
    try:
        if not path.exists():
            ensure_dir(path.parent)  # 確保資料夾存在
            path.touch()  # 建立空檔案
        return ResultCode.SUCCESS  # 成功
    except Exception as e:
        
        return ResultCode.TOOL_FILE_CREATE_FAILED  # 檔案創建失敗


@tool
def file_exists(path: Path) -> bool:
    """
    檢查檔案是否存在
    """
    return path.is_file()


@tool
def is_file_empty(path: Path) -> bool:
    """
    檢查檔案是否為空（0 bytes），並回傳結果。
    """
    try:
        return path.stat().st_size == 0
    except Exception as e:
        
        return ResultCode.TOOL_FILE_STAT_FAILED  # 檔案狀態檢查失敗


@tool
def clear_file(path: Path) -> int:
    """
    清空檔案內容（不刪檔）並回傳成功或錯誤碼。
    """
    try:
        if path.exists():
            path.write_text("", encoding="utf-8")  # 清空檔案
        return ResultCode.SUCCESS  # 成功
    except Exception:
        return ResultCode.TOOL_FILE_CLEAR_FAILED  # 清空檔案失敗
