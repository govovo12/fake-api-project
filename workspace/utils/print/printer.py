# workspace/utils/printer/printer.py

from datetime import datetime
from .color_helper import apply_color, OKGREEN, WARNING, FAIL

def tool(func):
    func.is_tool = True
    return func

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def _format_prefix(level: str) -> str:
    now = datetime.now().strftime(TIME_FORMAT)
    return f"[{now}] {level.upper():<5}"

@tool
def print_info(message: str):
    """彩色 info log 輸出，含時間 [TOOL]"""
    prefix = apply_color(_format_prefix("INFO"), OKGREEN)
    print(f"{prefix} - {message}")

@tool
def print_warn(message: str):
    """彩色 warn log 輸出，含時間 [TOOL]"""
    prefix = apply_color(_format_prefix("WARN"), WARNING)
    print(f"{prefix} - {message}")

@tool
def print_error(message: str):
    """彩色 error log 輸出，含時間 [TOOL]"""
    prefix = apply_color(_format_prefix("ERROR"), FAIL)
    print(f"{prefix} - {message}")
