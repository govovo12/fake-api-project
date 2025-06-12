from pathlib import Path
from workspace.config.rules.error_codes import ResultCode
from workspace.utils.data.data_loader import save_json  # 從 data_loader 引入 save_json

# ✅ 工具函式標記（供 tools_table 掃描用）
def tool(func):
    func.is_tool = True
    return func


@tool
def write_empty_data_file(path: Path, data: dict) -> int:
    """
    建立空白資料檔案，根據傳入的資料結構寫入檔案。
    - data 是一個字典，包含測試資料的結構和初始值。
    """
    try:
        # 儲存資料
        return save_json(path, data)  # 回傳 save_json 的結果
    except Exception:
        return ResultCode.TOOL_USER_TESTDATA_FILE_WRITE_FAILED

