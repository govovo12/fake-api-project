from typing import Optional

from workspace.utils.file.file_helper import generate_testdata_path, save_json
from workspace.utils.retry.retry_handler import safe_call
from workspace.config.rules.error_codes import ResultCode


def write_user_data(uuid: str) -> Optional[int]:
    """
    將使用者 UUID 寫入對應測資檔案中。

    成功 → 不回傳  
    失敗 → 回傳錯誤碼（ResultCode）
    """
    try:
        path = generate_testdata_path("user", uuid)
        code = safe_call(save_json, path, {"user_uuid": uuid})
        if code is not None:
            return code

        return ResultCode.SUCCESS

    except Exception as e:
        print(f"[DEBUG] write_user_data 例外：{type(e).__name__} - {str(e)}")
        return ResultCode.UNKNOWN_FILE_SAVE_ERROR
