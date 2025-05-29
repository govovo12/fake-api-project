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

def send_message(msg):
    """
    發送 Telegram 通知。
    """
    notifier = NotifierFactory.get_notifier()
    if notifier:
        notifier.send(msg)

def process_api_exception(e):
    """
    統一處理 API 錯誤
    """
    return process_exception(e, context="api")

def process_unknown_exception(e):
    """
    統一處理未知錯誤
    """
    return process_exception(e, context="unknown")
