"""
任務模組：刪除購物車測資檔案

流程說明：
- 根據 UUID 取得對應測資檔案路徑
- 嘗試刪除檔案，捕捉錯誤
- 成功回傳 ResultCode.SUCCESS，否則回傳自定失敗碼
"""

# ------------------------
# 📦 錯誤碼與路徑
# ------------------------
from pathlib import Path
from workspace.config.paths import get_cart_path
from workspace.config.rules.error_codes import ResultCode

# ------------------------
# 🧰 工具模組
# ------------------------
from workspace.utils.file.file_helper import delete_file


def remove_cart_data(uuid: str) -> int:
    """
    移除對應 UUID 的購物車測資檔案。

    Args:
        uuid (str): 對應購物車測資的 UUID。

    Returns:
        int: ResultCode.SUCCESS 若成功刪除，否則回傳任務層級錯誤碼。
    """
    path: Path = get_cart_path(uuid)

    try:
        code = delete_file(path)
    except Exception:
        return ResultCode.REMOVE_CART_DATA_FAILED

    if code != ResultCode.SUCCESS:
        return ResultCode.REMOVE_CART_DATA_FAILED

    return ResultCode.SUCCESS
