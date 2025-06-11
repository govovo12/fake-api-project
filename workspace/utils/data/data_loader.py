import json
from pathlib import Path
from workspace.config.rules.error_codes import ResultCode

def load_json(path: Path):
    """
    讀取 JSON 檔案並回傳資料。
    若檔案不存在、無法解析或格式錯誤，回傳對應的錯誤碼。
    """
    if not path.exists():
        return ResultCode.TOOL_FILE_LOAD_FAILED  # 檔案不存在，返回錯誤碼

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 確保讀取到的資料是字典型態
        if not isinstance(data, dict):
            return ResultCode.TOOL_INVALID_FILE_DATA  # 返回錯誤碼

        return data  # 成功，回傳資料

    except json.JSONDecodeError:
        return ResultCode.TOOL_FILE_LOAD_FAILED  # JSON 格式錯誤，返回錯誤碼
    except PermissionError:
        return ResultCode.TOOL_FILE_PERMISSION_DENIED  # 權限錯誤，返回錯誤碼
    except Exception:
        return ResultCode.TOOL_FILE_LOAD_FAILED  # 未知錯誤，返回錯誤碼
