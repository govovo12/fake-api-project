# log_helper.py
# --------------------------------------------------
# 根據錯誤碼類型輸出彩色狀態，同步寫入 logger（for CLI + pytest-html）
# 支援：成功碼、工具錯誤、任務錯誤、通用錯誤、未知錯誤
# --------------------------------------------------

import logging
from typing import Optional
from workspace.config.rules.error_codes import (
    ResultCode,
    SUCCESS_CODES,
    TOOL_ERROR_CODES,
    TASK_ERROR_CODES,
    GENERIC_ERROR_CODES,
    ERROR_MESSAGES,
)

# 初始化 logger 實體
logger = logging.getLogger(__name__)


def log_simple_result(code: int, context: Optional[str] = None) -> None:
    """
    根據錯誤碼輸出對應狀態與訊息，同時寫入 CLI 與 logger

    Args:
        code (int): 錯誤碼
        context (Optional[str]): 額外描述內容，例如模組/步驟
    """
    # ✅ 取得訊息，若找不到則 fallback 為 "未知錯誤"
    msg = ERROR_MESSAGES.get(code)
    if msg is None:
        msg = "未知錯誤"


    # ✅ 錯誤碼分類 + 狀態圖示
    if code in SUCCESS_CODES:
        status = "✅ 成功"
    elif code in TOOL_ERROR_CODES:
        status = "❌ 工具錯誤"
    elif code in TASK_ERROR_CODES:
        status = "▲ 任務錯誤"
    elif code in GENERIC_ERROR_CODES:
        status = "❓ 通用錯誤"
    else:
        status = "❓ 未知類型"

    # ✅ 格式化輸出訊息
    full_msg = f"[{status}] (code={code}, msg={msg})"
    if context:
        full_msg += f" - {context}"

    # CLI 印出 + logger 寫入（供 pytest-html 報表使用）
    print(full_msg)
    logger.info(full_msg)
    
