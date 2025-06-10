from pathlib import Path
from workspace.config.rules.error_codes import ResultCode, TaskModuleError
from workspace.utils.file.file_helper import save_json

# ✅ 工具函式標記（供 tools_table 掃描用）
def tool(func):
    func.is_tool = True
    return func


@tool
def write_empty_data_file(path: Path, kind: str) -> None:
    """
    建立空白資料檔案，根據 kind 產生初始結構並寫入檔案。
    kind 可為 'user' 或 'product'。
    """
    empty_content = {}

    if kind == "user":
        empty_content = {"users": []}
    elif kind == "product":
        empty_content = {"products": []}
    else:
        raise TaskModuleError(ResultCode.INVALID_FILE_KIND)

    try:
        save_json(path, empty_content)
    except TaskModuleError as e:
        raise TaskModuleError(e.code)  # 轉拋原始錯誤碼
    except Exception:
        raise TaskModuleError(ResultCode.USER_TESTDATA_FILE_WRITE_FAILED)
