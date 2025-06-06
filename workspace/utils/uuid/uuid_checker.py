from pathlib import Path
from workspace.utils.file.file_helper import file_exists, is_file_empty

TESTDATA_PATH = Path("workspace/testdata")
USER_PATH = TESTDATA_PATH / "user"
PRODUCT_PATH = TESTDATA_PATH / "product"

def check_if_testdata_exists(uuid: str) -> bool:
    """
    檢查是否已存在該 uuid 對應的 user 與 product 測資檔案
    （存在且非空才算存在）

    Args:
        uuid (str): UUID 字串

    Returns:
        bool: True 表示已存在，不可使用；False 表示尚未使用，可用
    """
    user_file = USER_PATH / f"{uuid}.json"
    product_file = PRODUCT_PATH / f"{uuid}.json"
    return all([
        file_exists(user_file) and not is_file_empty(user_file),
        file_exists(product_file) and not is_file_empty(product_file),
    ])
