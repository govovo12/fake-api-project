from utils.print.printer import print_info, print_warn, print_error
from utils.logger.log_writer import write_log

# === Log 工具：印出並交給 log_writer 寫入 run_log.txt ===
def log_info(message: str):
    print_info(message)
    write_log("INFO", message)

def log_warn(message: str):
    print_warn(message)
    write_log("WARN", message)

def log_error(message: str, code: str = None):
    formatted = f"[{code}] {message}" if code else message
    print_error(formatted)
    write_log("ERROR", formatted)