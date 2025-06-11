from pathlib import Path
from workspace.config.rules.error_codes import ResultCode
from workspace.utils.file.file_helper import save_json

# ✅ 工具函式標記（供 tools_table 掃描用）
def tool(func):
    func.is_tool = True
    return func


@tool
def write_empty_data_file(path: Path, data: dict) -> None:
    """
    建立空白資料檔案，根據傳入的資料結構寫入檔案。
    - data 是一個字典，包含測試資料的結構和初始值。
    """
    try:
        # 儲存資料
        save_json(path, data)
    except Exception as e:
        
        return ResultCode.USER_TESTDATA_FILE_WRITE_FAILED
