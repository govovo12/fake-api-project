from typing import Tuple, Optional
from workspace.utils.file.file_helper import save_json, file_exists
from workspace.config.paths import USER_TESTDATA_ROOT
from workspace.config.rules.error_codes import ResultCode, REASON_CODE_MAP
from pathlib import Path

def write_user_data(uuid: str, user_data: dict) -> Tuple[int, Optional[None], Optional[dict]]:
    """
    子組合器：儲存使用者測資至正式測資資料夾
    回傳格式：code, None, meta or None
    """

    user_path = USER_TESTDATA_ROOT / f"{uuid}.json"

    # Step 1: 判斷路徑是否存在
    if not user_path.parent.exists():
        return ResultCode.USER_TESTDATA_SAVE_FAILED, None, {
            "reason": "dir_not_found",
            "path": str(user_path.parent)
        }

    # Step 2: 儲存資料
    success, meta = save_json(user_path, user_data)
    if not success:
        reason = meta.get("reason", "")
        code = REASON_CODE_MAP.get(reason, ResultCode.USER_TESTDATA_SAVE_FAILED)
        return code, None, meta

    return ResultCode.SUCCESS, None, None
