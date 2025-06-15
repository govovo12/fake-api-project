from workspace.config.rules.error_codes import ResultCode
from workspace.modules.register.register_user import register_user
from workspace.utils.logger.log_helper import log_simple_result


def register_user_with_log(uuid: str, url: str, headers: dict) -> int:
    """
    子控制器：呼叫 register_user 任務模組，處理錯誤碼與 log 輸出。
    成功回傳 REGISTER_TASK_SUCCESS（10001），否則原樣回傳底層錯誤碼。

    :param uuid: 使用者測資對應的識別碼
    :param url: 註冊 API 完整網址
    :param headers: API 請求所需 headers
    :return: int 統一錯誤碼
    """
    result_code = register_user(uuid, url, headers)
    log_simple_result(result_code)

    if result_code == 0:
        return ResultCode.REGISTER_TASK_SUCCESS

    return result_code
