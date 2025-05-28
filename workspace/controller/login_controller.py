# workspace/controller/login_controller.py

from modules.login.login_reader import read_login_requests
from modules.login.login_executor import execute_login
from modules.login.login_token_writer import store_token
from modules.login.login_schema import LoginResult
from config.rules.error_codes import ERROR_MESSAGES
from utils.print.printer import print_info, print_warn, print_errorfrom controller.account_generator_controller import run_account_generator_task
from typing import List


# TODO: ⚠ 暫時自動產生帳號測資，未來主流程完成後請改由外部注入

def run_login_task() -> List[LoginResult]:
    run_account_generator_task()
    login_requests = read_login_requests()
    results = []

    for req in login_requests:
        result = execute_login(req)
        results.append(result)

        if result.success:
            store_token(result)
            print_info(f"登入成功: {req.username}")
        else:
            msg = ERROR_MESSAGES.get(result.error_code, "未知錯誤")
            print_error(f"登入失敗: {req.username} | 錯誤碼 {result.error_code} | {msg}")

    return results


if __name__ == "__main__":
    run_login_task()
