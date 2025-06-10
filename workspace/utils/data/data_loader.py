import json
from pathlib import Path
from workspace.config.rules.error_codes import ResultCode, TaskModuleError

# ✅ 工具函式標記（供 tools_table 掃描用）
def tool(func):
    func.is_tool = True
    return func


@tool
def load_json(path: Path) -> dict:
    """
    讀取 JSON 檔案並回傳 dict。
    若檔案不存在、無法解析或格式錯誤，拋出 TaskModuleError。
    """
    if not path.exists():
        raise TaskModuleError(ResultCode.FILE_NOT_FOUND)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise TaskModuleError(ResultCode.INVALID_FILE_DATA)

        return data

    except json.JSONDecodeError:
        raise TaskModuleError(ResultCode.FILE_LOAD_FAILED)

    except PermissionError:
        raise TaskModuleError(ResultCode.FILE_PERMISSION_DENIED)

    except Exception:
        raise TaskModuleError(ResultCode.UNKNOWN_FILE_LOAD_ERROR)
