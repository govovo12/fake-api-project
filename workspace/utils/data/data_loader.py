# workspace/utils/data/data_loader.py

from pathlib import Path
from typing import Optional, Tuple
from workspace.utils.file import file_helper

# ✅ 工具函式裝飾器：內建於模組中（非 import）
def tool(func):
    func.is_tool = True
    return func


@tool
def load_json(path_or_str: str | Path) -> Tuple[bool, Optional[dict], Optional[dict]]:
    """
    通用 JSON 讀取器，明確區分：不存在 / 格式錯誤 / 空內容。
    """
    path = Path(path_or_str)

    # ✅ 正確責任：路徑不存在
    if not path.exists():
        return False, None, {
            "reason": "file_not_found",
            "message": "指定的 JSON 檔案不存在",
            "path": str(path)
        }

    try:
        data = file_helper.load_json(path)

        # ✅ 正確責任：存在但內容為 None（可能是空檔或格式錯）
        if data is None:
            return False, None, {
                "reason": "file_empty_or_invalid",
                "message": "檔案內容為 None，可能為空或非 JSON",
                "path": str(path)
            }

        return True, data, None

    except Exception as e:
        return False, None, {
            "reason": "load_json_failed",
            "message": str(e),
            "path": str(path)
        }




@tool
def save_json(data: dict, path_or_str: str | Path) -> Tuple[bool, Optional[dict]]:
    """
    通用 JSON 寫入器，成功回傳 True，失敗回傳錯誤資訊
    """
    path = Path(path_or_str)
    try:
        result = file_helper.save_json(data, path)
        return result, None if result else {
            "reason": "save_returned_false",
            "message": "file_helper.save_json 回傳 False",
            "path": str(path)
        }
    except PermissionError as e:
        return False, {
            "reason": "permission_denied",
            "message": str(e),
            "path": str(path)
        }
    except UnicodeEncodeError as e:
        return False, {
            "reason": "encoding_error",
            "message": str(e),
            "path": str(path)
        }
    except Exception as e:
        return False, {
            "reason": "unknown_exception",
            "message": str(e),
            "path": str(path)
        }
