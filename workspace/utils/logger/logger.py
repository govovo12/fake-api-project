from utils.printer import print_info, print_warn, print_error
from config.paths import LOG_PATH
from utils.logger.log_writer import write_log  # optional if used

# 示意版，若未連結 log_writer 功能，保留純印出接口

def log_info(message: str):
    print_info(message)

def log_warn(message: str):
    print_warn(message)

def log_error(message: str, code: str = None):
    formatted = f"[{code}] {message}" if code else message
    print_error(formatted)
