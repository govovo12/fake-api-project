from workspace.modules.register.register_user import register_user
from workspace.utils.logger.log_helper import log_step_result
from workspace.config.rules.error_codes import ResultCode


__task_info__ = {
    "name": "註冊模組",
    "function": "user_register_controller",
    "uuid_required": True
}


def user_register_controller(uuid: str) -> tuple[int, int | None]:
    """
    控制器：註冊流程（透過組合器）
    - 呼叫 register_user(uuid)
    - 回傳 code 與註冊 ID（成功時）
    """

    log_step_result("開始註冊流程", ResultCode.REGISTER_STEP_BUILD_PAYLOAD)

    code, user_id = register_user(uuid)

    log_step_result("註冊流程結束", code)

    return code, user_id
