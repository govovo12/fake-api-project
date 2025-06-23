from workspace.controller.user_login_controller import login_and_report
from workspace.utils.logger.trace_helper import print_trace
from workspace.controller.data_generation_controller import generate_user_and_product_data
from workspace.controller.user_registration_controller import register_user_with_log
from workspace.utils.uuid.uuid_generator import generate_batch_uuid_with_code
from workspace.config.rules.error_codes import ResultCode
from workspace.controller.product_controller import create_product_and_report
from workspace.controller.cart_controller import create_cart_and_report
from workspace.controller.clear_testdata_controller import clear_user_and_product_data  


def run(headers: dict, url: str, login_cred: dict) -> int:
    """
    總控制器：執行 Fake Store 測資產生 + 註冊 + 登入任務
    """
    print_trace("[STEP 1] 產生 UUID")
    uuid = generate_batch_uuid_with_code()
    if not isinstance(uuid, str):
        return ResultCode.UUID_GEN_FAIL


    print_trace("[STEP 2] 執行測資產生任務")
    code = generate_user_and_product_data(uuid)
    if code != ResultCode.TESTDATA_TASK_SUCCESS:
        return code

    print_trace("[STEP 3] 執行註冊任務")
    code = register_user_with_log(uuid, url, headers)
    if code != ResultCode.REGISTER_TASK_SUCCESS:
        return code

    print_trace("[STEP 4] 執行登入任務")
    code, token = login_and_report(login_cred, headers)
    if code != ResultCode.LOGIN_TASK_SUCCESS:
        return code

    print_trace(f"成功取得 token：{token}")

    print_trace("[STEP 5] 執行建立商品任務")
    code, _ = create_product_and_report(uuid, token)
    if code != ResultCode.CREATE_PRODUCT_SUCCESS:
        return code

    print_trace("[STEP 6] 執行建立購物車任務")
    code, _ = create_cart_and_report(uuid, token)
    if code != ResultCode.CREATE_CART_SUCCESS:
        return code

    print_trace("[STEP 7] 執行清除測資任務")
    code = clear_user_and_product_data(uuid)
    if code != ResultCode.TASK_CLEAN_TESTDATA_SUCCESS:
        return code

    return ResultCode.MASTER_TASK_SUCCESS

