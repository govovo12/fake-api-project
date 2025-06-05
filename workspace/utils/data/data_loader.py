# workspace/utils/data/data_loader.py

from pathlib import Path
import json
from workspace.utils.print.printer import print_error
from workspace.utils.file import file_helper
from workspace.config import paths
from workspace.config.rules import error_codes
from workspace.config.rules.error_codes import ResultCode

def tool(func):
    func.is_tool = True
    return func

@tool
def load_json(path_or_str: str | Path):
    """通用 JSON 讀取器，回傳 (code, data)"""
    try:
        data = file_helper.load_json(path_or_str)
        return 0, data
    except Exception as e:
        print_error(f"❌ JSON 讀取失敗：{e}")
        return error_codes.ResultCode.USER_TESTDATA_NOT_FOUND, None

@tool
def save_json(data: dict, path_or_str: str | Path):
    """通用 JSON 寫入器"""
    try:
        file_helper.save_json(data, path_or_str)
        return 0
    except Exception as e:
        print_error(f"❌ JSON 寫入失敗：{e}")
        return error_codes.ResultCode.USER_WRITE_FAIL

@tool
def load_user_testdata(uuid: str):
    """根據 UUID 讀取 user 測資檔案"""
    user_path = paths.get_user_testdata_path(f"{uuid}_user.json")
    return load_json(user_path)

@tool
def load_product_testdata(uuid: str):
    """根據 UUID 讀取 product 測資檔案"""
    product_path = paths.get_product_testdata_path(f"{uuid}_product.json")
    return load_json(product_path)

def save_json(data: dict, path_or_str: str | Path) -> None:
    """寫入 JSON 檔（由 file_helper 實作）"""
    try:
        file_helper.save_json(data, path_or_str)
    except Exception as e:
        raise RuntimeError(f"❌ JSON 寫入失敗：{e}")

def load_json(path_or_str: str | Path) -> tuple[int, dict]:
    """讀取 JSON 檔，錯誤時回傳錯誤碼與空 dict"""
    try:
        data = file_helper.load_json(path_or_str)
        return ResultCode.SUCCESS, data
    except Exception as e:
        print(f"❌ JSON 讀取失敗：{e}")
        return ResultCode.USER_TESTDATA_NOT_FOUND, {}