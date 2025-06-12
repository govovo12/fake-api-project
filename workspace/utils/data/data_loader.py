import json
from pathlib import Path
from workspace.config.rules.error_codes import ResultCode

# ✅ 工具函式標記（供 tools_table 掃描用）
def tool(func):
    func.is_tool = True
    return func


def load_json(path: Path) -> dict:
    """
    讀取 JSON 檔案並回傳 dict。
    若檔案不存在、無法解析或格式錯誤，回傳對應的錯誤碼。
    """
    if not path.exists():
        print("檔案不存在！")  # Debug 輸出
        return ResultCode.TOOL_FILE_LOAD_FAILED  # 檔案不存在，返回錯誤碼

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 確保讀取到的資料是字典型態
        if not isinstance(data, dict):
            print("資料格式錯誤！")  # Debug 輸出
            return ResultCode.TOOL_INVALID_FILE_DATA  # 返回錯誤碼

        return data  # 返回字典資料

    except json.JSONDecodeError:
        print("JSON 格式錯誤！")  # Debug 輸出
        return ResultCode.TOOL_FILE_LOAD_FAILED  # JSON 格式錯誤，返回錯誤碼
    except PermissionError:
        print("捕獲到檔案權限錯誤！")  # Debug 輸出
        return ResultCode.TOOL_FILE_PERMISSION_DENIED  # 權限錯誤，返回錯誤碼
    except Exception as e:
        print(f"捕獲到其他錯誤：{e}")  # Debug 輸出
        return ResultCode.TOOL_FILE_LOAD_FAILED  # 未知錯誤，返回錯誤碼




@tool
def save_json(path: Path, data: dict) -> int:
    """
    儲存資料為 JSON 格式。
    儲存成功回傳 SUCCESS，失敗回傳錯誤碼。
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return ResultCode.SUCCESS  # 成功，回傳 success code

    except Exception:
        return ResultCode.TOOL_FILE_WRITE_FAILED  # 返回錯誤碼
