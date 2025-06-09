import json
from pathlib import Path
from workspace.config.rules.error_codes import ResultCode
from workspace.utils.file.file_helper import save_json

def write_empty_data_file(path: Path, kind: str) -> tuple[bool, dict]:
    """
    建立空白資料檔案，根據 kind 可調整空白結構
    """
    try:
        empty_content = {}

        # 可依 kind 產生不同空白內容
        if kind == "user":
            empty_content = {
                "users": []
            }
        elif kind == "product":
            empty_content = {
                "products": []
            }

        success = save_json(path, empty_content)
        if not success:
            return False, {
                "code": ResultCode.USER_TESTDATA_FILE_WRITE_FAILED,
                "message": "save_json 返回 False"
            }
        return True, {}
    except Exception as e:
        return False, {
            "code": ResultCode.USER_TESTDATA_FILE_WRITE_FAILED,
            "message": f"寫入空白資料檔案例外：{e}"
        }
