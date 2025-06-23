"""
子控制器：建立商品流程控制模組

職責：
- 呼叫任務模組 create_product()
- 加入 retry 機制（可恢復錯誤碼）
- 印出最終錯誤碼
- 成功轉換為 CREATE_PRODUCT_SUCCESS，失敗則回傳原錯誤碼
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
from workspace.modules.product.create_product import create_product


def create_product_and_report(uuid: str, token: str) -> tuple[int, dict | None]:
    """
    子控制器：建立商品（含 retry 與錯誤碼轉換）

    Args:
        uuid (str): 商品測資檔 UUID
        token (str): Bearer token

    Returns:
        tuple[int, dict | None]: 最終錯誤碼（含轉換）、回應資料
    """
    create_with_retry = retry_on_code(
        lambda u: create_product(u, token),
        retry_codes=[
            ResultCode.SERVER_ERROR,
            ResultCode.REQUESTS_EXCEPTION
        ],
        max_retries=3,
        delay=0.1
    )

    code, response = create_with_retry(uuid)

    if code != ResultCode.SUCCESS:
        log_simple_result(code)
        return code, None

    log_simple_result(ResultCode.CREATE_PRODUCT_SUCCESS)
    return ResultCode.CREATE_PRODUCT_SUCCESS, response
