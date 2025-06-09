from typing import Optional, Tuple
from workspace.utils.file.file_helper import generate_testdata_path
from workspace.utils.file.file_helper import save_json
from workspace.config.rules.error_codes import ResultCode, REASON_CODE_MAP


def write_user_data(uuid: str, data: dict) -> Tuple[int, Optional[str], Optional[dict]]:
    """
    子組合器：將使用者測資儲存為 JSON 檔案
    """
    path, meta_path = generate_testdata_path("user", uuid)

    if path is None:
        reason = meta_path.get("reason", "")
        code = REASON_CODE_MAP.get(reason, ResultCode.USER_TESTDATA_SAVE_FAILED)  # ✅ fallback 合理設計
        return code, None, meta_path

    success, meta = save_json(path, data)
    if not success:
        reason = meta.get("reason", "")
        code = REASON_CODE_MAP.get(reason, ResultCode.USER_TESTDATA_FILE_WRITE_FAILED)
        return code, None, meta

    return ResultCode.SUCCESS, str(path), None
