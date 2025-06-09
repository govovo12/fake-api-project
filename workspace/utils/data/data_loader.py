import json
from pathlib import Path
from workspace.config.rules.error_codes import ResultCode

def load_json(path: Path) -> tuple[bool, dict | None]:
    """
    讀取 JSON 檔案，檢查檔案存在性與格式
    """
    if not path.exists():
        return False, {
            "code": ResultCode.FILE_NOT_FOUND,
            "message": f"找不到檔案：{path}"
        }

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return False, {
                "code": ResultCode.INVALID_FILE_DATA,
                "message": "檔案內容不是字典格式"
            }

        return True, data

    except json.JSONDecodeError as e:
        return False, {
            "code": ResultCode.FILE_LOAD_FAILED,
            "message": f"JSON 解碼失敗：{e}"
        }

    except PermissionError as e:
        return False, {
            "code": ResultCode.FILE_PERMISSION_DENIED,
            "message": f"檔案權限不足：{e}"
        }

    except Exception as e:
        return False, {
            "code": ResultCode.UNKNOWN_FILE_SAVE_ERROR,
            "message": f"不明錯誤：{e}"
        }
