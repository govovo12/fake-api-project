from typing import Tuple, Optional
from workspace.modules.fake_data.fake_user.user_generator import generate_user_data
from workspace.utils.data.data_enricher import enrich_with_uuid
from workspace.config.rules.error_codes import ResultCode, ResultCode


def build_user_data(uuid: str) -> Tuple[int, Optional[dict], Optional[dict]]:
    """
    子組合器：產生使用者測資並附加 UUID
    回傳格式：code, user_data or None, meta or None
    """
    success, user_data, meta = generate_user_data()
    if not success:
        reason = meta.get("reason", "")
        code = ResultCode.get(reason, ResultCode.USER_GENERATION_FAILED)
        return code, None, meta

    success, user_with_uuid, meta = enrich_with_uuid(user_data, uuid)
    if not success:
        reason = meta.get("reason", "")
        code = ResultCode.get(reason, ResultCode.USER_UUID_ATTACH_FAILED)
        return code, None, meta

    return ResultCode.SUCCESS, user_with_uuid, None
