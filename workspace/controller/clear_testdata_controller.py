"""
子控制器：清除測資檔案（user, product, cart）
"""

# ------------------------
# 📦 錯誤碼與常數
# ------------------------
from workspace.config.rules.error_codes import ResultCode

# ------------------------
# 🧰 工具模組
# ------------------------
from workspace.utils.retry.retry_handler import retry_on_code
from workspace.utils.logger.log_helper import log_simple_result

# ------------------------
# 🔨 任務模組
# ------------------------
from workspace.modules.cleaner.remove_user_data import remove_user_data
from workspace.modules.cleaner.remove_product_data import remove_product_data
from workspace.modules.cleaner.remove_cart_data import remove_cart_data


def clear_user_and_product_data(uuid: str) -> int:
    """
    清除指定 UUID 的使用者、商品與購物車測資。

    Args:
        uuid (str): 測資對應 UUID

    Returns:
        int: 成功則回傳 TASK_CLEAN_TESTDATA_SUCCESS，否則回傳錯誤碼
    """
    remove_user = retry_on_code(
        lambda u: remove_user_data(u),
        retry_codes=[ResultCode.TOOL_FILE_DELETE_FAILED],
        max_retries=3,
        delay=0.1,
    )
    remove_product = retry_on_code(
        lambda u: remove_product_data(u),
        retry_codes=[ResultCode.TOOL_FILE_DELETE_FAILED],
        max_retries=3,
        delay=0.1,
    )
    remove_cart = retry_on_code(
        lambda u: remove_cart_data(u),
        retry_codes=[ResultCode.TOOL_FILE_DELETE_FAILED],
        max_retries=3,
        delay=0.1,
    )

    code = remove_user(uuid)
    if code != ResultCode.SUCCESS:
        log_simple_result(code)
        return code

    code = remove_product(uuid)
    if code != ResultCode.SUCCESS:
        log_simple_result(code)
        return code

    code = remove_cart(uuid)
    if code != ResultCode.SUCCESS:
        log_simple_result(code)
        return code

    log_simple_result(ResultCode.TASK_CLEAN_TESTDATA_SUCCESS)
    return ResultCode.TASK_CLEAN_TESTDATA_SUCCESS
