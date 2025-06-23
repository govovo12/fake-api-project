# -----------------------------
# 🧰 工具區（Log、追蹤、錯誤碼等）
# -----------------------------
from workspace.utils.logger.trace_helper import print_trace
from workspace.utils.logger.log_helper import log_simple_result
from workspace.config.rules.error_codes import ResultCode

# -----------------------------
# 🧩 模組區（組合器：User / Product / Cart）
# -----------------------------
from workspace.modules.fake_data.orchestrator.build_user_data_and_write import build_user_data_and_write
from workspace.modules.fake_data.orchestrator.build_product_data_and_write import build_product_data_and_write
from workspace.modules.fake_data.orchestrator.build_cart_data_and_write import build_cart_data_and_write


def generate_user_and_product_data(uuid: str) -> int:
    """
    子控制器：依照指定 UUID 產生使用者、商品與購物車測資。

    僅印出任務級成功或錯誤訊息，避免底層雜訊。
    """
    print_trace(f"UUID: {uuid}")

    code = build_user_data_and_write(uuid)
    if code != ResultCode.SUCCESS:
        log_simple_result(code)
        return code

    code = build_product_data_and_write(uuid)
    if code != ResultCode.SUCCESS:
        log_simple_result(code)
        return code

    code = build_cart_data_and_write(uuid)
    if code != ResultCode.SUCCESS:
        log_simple_result(code)
        return code

    log_simple_result(ResultCode.TESTDATA_TASK_SUCCESS)
    return ResultCode.TESTDATA_TASK_SUCCESS
