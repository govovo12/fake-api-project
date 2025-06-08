from typing import Tuple, Optional
from workspace.utils.file.file_helper import save_json, file_exists
from workspace.config.paths import PRODUCT_TESTDATA_ROOT
from workspace.config.rules.error_codes import ResultCode, REASON_CODE_MAP
from pathlib import Path

def write_product_data(uuid: str, product_data: dict) -> Tuple[int, Optional[None], Optional[dict]]:
    """
    子組合器：儲存商品測資至正式測資資料夾
    回傳格式：code, None, meta or None
    """

    product_path = PRODUCT_TESTDATA_ROOT / f"{uuid}.json"

    # Step 1: 判斷路徑是否存在
    if not product_path.parent.exists():
        return ResultCode.PRODUCT_TESTDATA_SAVE_FAILED, None, {
            "reason": "dir_not_found",
            "path": str(product_path.parent)
        }

    # Step 2: 儲存資料
    success, meta = save_json(product_path, product_data)
    if not success:
        reason = meta.get("reason", "")
        code = REASON_CODE_MAP.get(reason, ResultCode.PRODUCT_TESTDATA_SAVE_FAILED)
        return code, None, meta

    return ResultCode.SUCCESS, None, None
