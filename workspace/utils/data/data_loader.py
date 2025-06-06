# workspace/utils/data/data_loader.py

from pathlib import Path
from workspace.utils.file import file_helper
from workspace.config.rules.error_codes import ResultCode
from typing import Optional

def tool(func):
    func.is_tool = True
    return func

@tool
def load_json(path_or_str: str | Path) -> tuple[int, Optional[dict]]:
    """[TOOL] 通用 JSON 讀取器，回傳 (錯誤碼, 資料 or None)"""
    try:
        data = file_helper.load_json(Path(path_or_str))
        if data is None:
            return ResultCode.USER_TESTDATA_NOT_FOUND, None
        return ResultCode.SUCCESS, data
    except Exception:
        return ResultCode.USER_TESTDATA_NOT_FOUND, None

@tool
def save_json(data: dict, path_or_str: str | Path) -> int:
    """[TOOL] 通用 JSON 寫入器，成功回傳 0，失敗回傳錯誤碼"""
    try:
        success = file_helper.save_json(data, Path(path_or_str))
        return ResultCode.SUCCESS if success else ResultCode.USER_WRITE_FAIL
    except Exception:
        return ResultCode.USER_WRITE_FAIL
