"""
任務模組：刪除商品測資檔案
"""

# ------------------------
# 📦 錯誤碼與路徑
# ------------------------
from pathlib import Path
from workspace.config.paths import get_product_path
from workspace.config.rules.error_codes import ResultCode

# ------------------------
# 🧰 工具模組
# ------------------------
from workspace.utils.file.file_helper import delete_file


def remove_product_data(uuid: str) -> int:
    """
    移除對應 UUID 的商品測資檔案。

    Args:
        uuid (str): 對應商品測資的 UUID。

    Returns:
        int: ResultCode.SUCCESS 若成功刪除，否則回傳任務層級錯誤碼。
    """
    path: Path = get_product_path(uuid)

    try:
        code = delete_file(path)
    except Exception:
        return ResultCode.REMOVE_PRODUCT_DATA_FAILED

    if code != ResultCode.SUCCESS:
        return ResultCode.REMOVE_PRODUCT_DATA_FAILED

    return ResultCode.SUCCESS
