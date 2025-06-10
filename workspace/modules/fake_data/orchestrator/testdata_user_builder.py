from typing import Optional

from workspace.modules.fake_data.fake_user.user_generator import generate_user_data
from workspace.utils.data.data_enricher import enrich_with_uuid
from workspace.utils.retry.retry_handler import safe_call
from workspace.config.rules.error_codes import ResultCode


def build_user_data(uuid: str) -> Optional[int]:
    """
    建立使用者測資資料，並附加 UUID 欄位。

    成功 → 不回傳  
    失敗 → 回傳錯誤碼（ResultCode）
    """
    try:
        code = safe_call(generate_user_data, uuid)
        if code is not None:
            return code

        code = safe_call(enrich_with_uuid, {}, uuid)
        if code is not None:
            return code

        return ResultCode.SUCCESS

    except Exception as e:
        print(f"[DEBUG] build_user_data 例外：{type(e).__name__} - {str(e)}")
        return ResultCode.UNKNOWN_FILE_SAVE_ERROR
