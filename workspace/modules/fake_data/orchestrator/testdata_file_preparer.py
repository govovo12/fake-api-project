from typing import Tuple, Optional
from pathlib import Path
from workspace.utils.file.file_helper import ensure_dir, file_exists, save_json
from workspace.config.paths import USER_TESTDATA_ROOT, PRODUCT_TESTDATA_ROOT
from workspace.config.rules.error_codes import ResultCode


def prepare_testdata_files(uuid: str) -> Tuple[int, Optional[None], Optional[dict]]:
    """
    組合器：建立測資資料夾與對應的空白 JSON 檔案
    - 建立 workspace/testdata/user/{uuid}.json
    - 建立 workspace/testdata/product/{uuid}.json
    - 若任一已存在，則視為重複產生，回傳錯誤碼
    """
    try:
        ensure_dir(USER_TESTDATA_ROOT)
        ensure_dir(PRODUCT_TESTDATA_ROOT)
    except Exception as e:
        return ResultCode.TESTDATA_DIR_PREPARE_FAILED, None, {"reason": "mkdir_failed", "msg": str(e)}

    user_path = USER_TESTDATA_ROOT / f"{uuid}.json"
    product_path = PRODUCT_TESTDATA_ROOT / f"{uuid}.json"

    # 檢查是否已存在
    if file_exists(user_path) or file_exists(product_path):
        return ResultCode.TESTDATA_FILE_ALREADY_EXISTS, None, {
            "reason": "file_exists",
            "user_path": str(user_path),
            "product_path": str(product_path)
        }

    # 建立空白 JSON 檔案（預設寫入空 dict）
    success_u, meta_u = save_json(user_path, {})
    success_p, meta_p = save_json(product_path, {})

    if not success_u:
        return ResultCode.TESTDATA_USER_FILE_WRITE_FAILED, None, meta_u
    if not success_p:
        return ResultCode.TESTDATA_PRODUCT_FILE_WRITE_FAILED, None, meta_p

    return ResultCode.SUCCESS, None, None
