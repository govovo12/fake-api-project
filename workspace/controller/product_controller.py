from workspace.modules.product.create_product import create_product
from workspace.utils.logger.log_helper import log_simple_result
from workspace.utils.retry.retry_handler import retry_on_code
from workspace.config.rules.error_codes import ResultCode


def create_product_and_report(uuid: str, token: str) -> tuple[int, dict | None]:
    """
    子控制器：建立商品，含 retry 與錯誤碼 log
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
    log_simple_result(code)
    return code, response
