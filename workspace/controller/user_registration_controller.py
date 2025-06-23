# -----------------------------
# ⚠️ 錯誤碼
# -----------------------------
from workspace.config.rules.error_codes import ResultCode

# -----------------------------
# 🧪 註冊任務模組
# -----------------------------
from workspace.modules.register.register_user import register_user

# -----------------------------
# 🧾 印出工具
# -----------------------------
from workspace.utils.logger.log_helper import log_simple_result


def register_user_with_log(uuid: str, url: str, headers: dict) -> int:
    """
    子控制器：註冊使用者，負責控制流程與統一印出。

    - 呼叫 register_user 任務模組
    - 印出錯誤或任務級成功訊息
    - 回傳語意化錯誤碼
    """
    result_code = register_user(uuid, url, headers)

    if result_code != ResultCode.SUCCESS:
        log_simple_result(result_code)
        return result_code

    log_simple_result(ResultCode.REGISTER_TASK_SUCCESS)
    return ResultCode.REGISTER_TASK_SUCCESS
