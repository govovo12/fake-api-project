"""
子控制器：建立購物車流程控制模組
"""

# ------------------------
# 📦 錯誤碼與配置
# ------------------------
from workspace.config.rules.error_codes import ResultCode

# ------------------------
# 🧰 工具模組
# ------------------------
from workspace.utils.logger.log_helper import log_simple_result
from workspace.utils.retry.retry_handler import retry_on_code

# ------------------------
# 🔨 任務模組
# ------------------------
from workspace.modules.cart.create_cart import create_cart


def create_cart_and_report(uuid: str, token: str) -> tuple[int, dict | None]:
    """
    子控制器：建立購物車
    - 若任務模組回傳錯誤碼，直接回傳錯誤碼
    - 成功則轉為 CREATE_CART_SUCCESS
    """
    create_with_retry = retry_on_code(
        lambda u: create_cart(u, token),
        retry_codes=[
            ResultCode.SERVER_ERROR,
            ResultCode.REQUESTS_EXCEPTION,
        ],
        max_retries=3,
        delay=0.1,
    )

    code, response = create_with_retry(uuid)

    # 若失敗，直接回傳底層錯誤碼
    if code != 0:
        log_simple_result(code)
        return code, None

    # 成功，轉換為此子控的成功碼
    log_simple_result(ResultCode.CREATE_CART_SUCCESS)
    return ResultCode.CREATE_CART_SUCCESS, response
