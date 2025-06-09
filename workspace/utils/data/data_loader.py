from typing import Optional, Tuple
from pathlib import Path
import json


# ✅ 工具函式標記（供 tools_table 掃描用）
def tool(func):
    func.is_tool = True
    return func


@tool
def load_json(path_or_str: str) -> Tuple[Optional[dict], Optional[dict]]:
    """
    從指定路徑讀取 JSON 檔案，回傳 dict 或錯誤資訊。

    Returns:
        data: 成功則為 dict，否則為 None
        meta: 若錯誤則包含 reason / message / path
    """
    try:
        path = Path(path_or_str)
        if not path.exists():
            return None, {
                "reason": "file_not_found",
                "message": f"File not found: {path}"
            }

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                return None, {
                    "reason": "file_empty_or_invalid",
                    "message": f"File is empty or invalid: {path}"
                }

            try:
                data = json.loads(content)
                return data, None
            except json.JSONDecodeError as e:
                return None, {
                    "reason": "load_json_failed",
                    "message": str(e),
                    "path": str(path)
                }

    except PermissionError as e:
        return None, {
            "reason": "permission_denied",
            "message": str(e),
            "path": path_or_str
        }
    except Exception as e:
        return None, {
            "reason": "unknown_exception",
            "message": str(e),
            "path": path_or_str
        }


@tool
def save_json(path_or_str: str, data: dict) -> Tuple[bool, Optional[dict]]:
    """
    將 dict 寫入指定路徑為 JSON 檔案。

    Returns:
        success: 是否寫入成功
        meta: 若失敗則包含 reason / message / path
    """
    try:
        path = Path(path_or_str)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True, None
    except PermissionError as e:
        return False, {
            "reason": "permission_denied",
            "message": str(e),
            "path": str(path_or_str)
        }
    except TypeError as e:
        return False, {
            "reason": "json_serialization_failed",
            "message": str(e),
            "path": str(path_or_str)
        }
    except Exception as e:
        return False, {
            "reason": "save_returned_false",
            "message": str(e),
            "path": str(path_or_str)
        }
