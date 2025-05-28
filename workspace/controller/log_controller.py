from utils.logger.logger import log_info, log_warn, log_error

# 統一 Log 控制器：供任務模組呼叫，不需碰 log 底層

def info(message: str):
    log_info(message)

def warn(message: str):
    log_warn(message)

def error(message: str, code: str = None):
    log_error(message, code)

def retry(func_name: str, attempt: int, error: Exception):
    """
    Retry 專用紀錄函式，用於 retry_controller 記錄每次重試失敗的情況。
    """
    log_warn(f"[Retry] {func_name} 第 {attempt} 次嘗試失敗：{repr(error)}")
