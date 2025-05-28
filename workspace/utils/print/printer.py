# workspace/utils/printer/printer.py

from datetime import datetime
from .color_helper import apply_color, OKGREEN, WARNING, FAIL

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def _format_prefix(level: str) -> str:
    now = datetime.now().strftime(TIME_FORMAT)
    return f"[{now}] {level.upper():<5}"

def print_info(message: str):
    prefix = apply_color(_format_prefix("INFO"), OKGREEN)
    print(f"{prefix} - {message}")

def print_warn(message: str):
    prefix = apply_color(_format_prefix("WARN"), WARNING)
    print(f"{prefix} - {message}")

def print_error(message: str):
    prefix = apply_color(_format_prefix("ERROR"), FAIL)
    print(f"{prefix} - {message}")
