# workspace/utils/logger.py

from workspace.utils.printer import print_info, print_warn, print_error

def log_info(message: str):
    print_info(message)


def log_warn(message: str):
    print_warn(message)


def log_error(message: str, code: str = None):
    if code:
        print_error(f"[{code}] {message}")
    else:
        print_error(message)


# 使用方式
# from workspace.utils.logger import log_info, log_error
# log_info("帳號產生完成")
# log_error("帳號存檔失敗", code="ACCOUNT_SAVE_FAIL")