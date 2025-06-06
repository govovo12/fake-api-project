from workspace.config.envs.api import REGISTER_URL
from workspace.config.paths import USER_TESTDATA_ROOT
from workspace.modules.register.build_register_payload import build_register_payload
from workspace.utils.file.file_helper import read_json_file
from workspace.utils.request.request_handler import post
from workspace.utils.response.response_helper import get_data_field_from_response
from workspace.config.rules.error_codes import ResultCode


def register_user(uuid: str) -> tuple[int, int | None]:
    """
    註冊使用者流程組合器：
    1. 讀取測資
    2. 組裝 payload
    3. 發送註冊請求
    4. 驗證是否成功（data.id 存在）
    """

    # 讀取 user 測資
    try:
        user_path = USER_TESTDATA_ROOT / f"{uuid}.json"
        user_data = read_json_file(user_path)
    except Exception:
        return ResultCode.USER_DATA_NOT_FOUND, None

    # 組裝 payload
    payload = build_register_payload(user_data)
    if not payload:
        return ResultCode.REGISTER_PAYLOAD_BUILD_FAILED, None

    # 發送註冊請求
    response = post(url=REGISTER_URL, json=payload)
    if response is None:
        return ResultCode.REGISTER_REQUEST_FAILED, None

    # 擷取回傳 ID
    user_id = get_data_field_from_response(response, "id")
    if user_id is None:
        return ResultCode.REGISTER_REQUEST_FAILED, None

    return 0, user_id
