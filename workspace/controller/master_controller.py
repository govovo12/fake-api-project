from workspace.controller.user_login_controller import login_and_report
from workspace.utils.logger.trace_helper import print_trace
from workspace.utils.logger.log_helper import log_simple_result
from workspace.controller.data_generation_controller import generate_user_and_product_data
from workspace.controller.user_registration_controller import register_user_with_log
from workspace.utils.uuid.uuid_generator import generate_batch_uuid_with_code
from workspace.config.rules.error_codes import ResultCode
from workspace.controller.product_controller import create_product_and_report


def run(headers: dict, url: str, login_cred: dict) -> int:
    """
    總控制器：執行 Fake Store 測資產生 + 註冊 + 登入任務
    """
    print_trace("開始產生 UUID")
    uuid = generate_batch_uuid_with_code()
    if not isinstance(uuid, str):
        log_simple_result(uuid)
        return uuid

    log_simple_result(ResultCode.SUCCESS)

    # 測資產生任務
    print_trace("測資產生任務啟動")
    code = generate_user_and_product_data(uuid)
    log_simple_result(code)
    if code != ResultCode.TESTDATA_TASK_SUCCESS:
        return code

    # 註冊任務
    print_trace(f"註冊任務啟動：url={url}")
    print_trace(f"註冊 headers keys: {list(headers.keys())}")
    code = register_user_with_log(uuid, url, headers)
    log_simple_result(code)
    if code != ResultCode.REGISTER_TASK_SUCCESS:
        return code

    # 登入任務
    print_trace("登入任務啟動")
    code, token = login_and_report(login_cred, headers)
    log_simple_result(code)
    if code != ResultCode.LOGIN_TASK_SUCCESS:
        return code

    print_trace(f"成功取得 token：{token}")

     # 建立商品任務
    print_trace("建立商品任務啟動")
    code, _ = create_product_and_report(uuid, token)
    log_simple_result(code)
    if code != ResultCode.CREATE_PRODUCT_SUCCESS:
        return code

    return ResultCode.SUCCESS
