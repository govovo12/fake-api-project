from workspace.utils.error.error_handler import handle_exception
from workspace.utils.notifier.factory import NotifierFactory
from workspace.controller import log_controller

def process_exception(e, context="system"):
    """
    統一處理例外，包含：格式轉換、紀錄 log、發送通知。
    """
    result = handle_exception(e)
    error_type = result.get("type", "unknown")
    code = result.get("code", "UNKNOWN")
    msg = result.get("msg", str(e))

    log_msg = f"[{context.upper()} ERROR] [{error_type}] ({code}) {msg}"
    log_controller.error(log_msg)  # 集中寫入錯誤 log
    send_message(log_msg)  # 發送到 Telegram

    return result