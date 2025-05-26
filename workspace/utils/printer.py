# workspace/utils/printer.py

from datetime import datetime

# 可調整的時間格式
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def _format_prefix(level: str) -> str:
    now = datetime.now().strftime(TIME_FORMAT)
    return f"[{now}] {level.upper():<5}"

def print_info(message: str):
    print(f"{_format_prefix('INFO')} - {message}")

def print_warn(message: str):
    print(f"{_format_prefix('WARN')} - {message}")

def print_error(message: str):
    print(f"{_format_prefix('ERROR')} - {message}")

# 範例用法（移除後可作為註解）
# from workspace.utils.printer import print_info, print_error
# print_info("開始產生帳號")
# print_error("帳號寫入失敗")
