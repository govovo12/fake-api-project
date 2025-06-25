from pathlib import Path
from workspace.config.rules.error_codes import ResultCode

def tool(func):
    func.is_tool = True
    return func

@tool
def stub_valid_json_file() -> str:
    """
    回傳一個有效的 JSON 檔案路徑字串（假資料示範用）
    """
    return "tests/unit/fake_data_stub/test_valid.json"


@tool
def stub_invalid_json_file() -> int:
    """
    寫入一個格式錯誤的 JSON 檔案，用於測試失敗情境。
    寫入成功回傳 ResultCode.SUCCESS，失敗回傳錯誤碼。
    """
    file_path = Path("tests/unit/fake_data_stub/test_invalid.json")
    try:
        file_path.write_text("{invalid json:", encoding="utf-8")
        return ResultCode.SUCCESS
    except Exception:
        return ResultCode.TOOL_STUB_FILE_WRITE_FAILED


@tool
def stub_valid_json_dict() -> dict:
    """
    回傳一個有效的 JSON 格式字典，供測試使用
    """
    return {"name": "R88", "version": "1.0", "enabled": True}


@tool
def stub_invalid_json_dict() -> dict:
    """
    回傳一個格式不完整的字典（假資料示範）
    """
    return {"name": "R88", "version": None, "enabled": "yes"}


@tool
def stub_invalid_input(data) -> int:
    """
    示範一個接受輸入參數並檢查的函式
    如果輸入不合法，回傳錯誤碼；否則回成功碼
    """
    if not isinstance(data, dict):
        return ResultCode.TOOL_STUB_INVALID_DATA
    # 假設其他驗證邏輯
    return ResultCode.SUCCESS
