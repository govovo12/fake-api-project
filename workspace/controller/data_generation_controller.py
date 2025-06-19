from workspace.utils.logger.trace_helper import print_trace
from workspace.utils.logger.log_helper import log_simple_result
from workspace.modules.fake_data.orchestrator.build_user_data_and_write import build_user_data_and_write
from workspace.modules.fake_data.orchestrator.build_product_data_and_write import build_product_data_and_write
from workspace.modules.fake_data.orchestrator.build_cart_data_and_write import build_cart_data_and_write
from workspace.config.rules.error_codes import ResultCode


def generate_user_and_product_data(uuid: str) -> int:
    """
    子控制器：根據 uuid 產生 user、product、cart 測資，負責 log 與錯誤碼轉譯。
    - 印出 trace log
    - 呼叫三個組合器（user, product, cart）
    - 回傳測資任務成功 or 中斷錯誤碼
    """
    print_trace(f"UUID: {uuid}")  # ✅ 傳一個 str 給 step 參數即可

    code = build_user_data_and_write(uuid)
    log_simple_result(code)
    if code != ResultCode.SUCCESS:
        return code

    code = build_product_data_and_write(uuid)
    log_simple_result(code)
    if code != ResultCode.SUCCESS:
        return code

    code = build_cart_data_and_write(uuid)
    log_simple_result(code)
    if code != ResultCode.SUCCESS:
        return code

    log_simple_result(ResultCode.TESTDATA_TASK_SUCCESS)
    print(f"✅ 測資產生流程完成，UUID: {uuid}")
    return ResultCode.TESTDATA_TASK_SUCCESS
