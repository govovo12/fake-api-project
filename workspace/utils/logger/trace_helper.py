# trace_helper.py
# ----------------------------------------
# 用於流程追蹤的工具模組，支援 CLI 印出與 pytest-html 報表同步記錄
# ----------------------------------------

import logging  # Python 內建 logging 模組，用於寫入 pytest-html 報表或 log 檔
from typing import Optional

# 建立 logger 實體
logger = logging.getLogger(__name__)


def print_trace(step: str, note: Optional[str] = None) -> None:
    """
    印出流程追蹤資訊，並同步寫入 logger 供 pytest-html 捕捉

    Args:
        step (str): 當前執行階段的步驟描述
        note (Optional[str]): 額外補充訊息（如 uuid、流程資訊）
    """
    full_msg = f"[TRACE] {step}"
    if note:
        full_msg += f" - {note}"

    print(full_msg)       # CLI 即時顯示
    logger.info(full_msg) # 寫入 pytest-html 報表 or log 檔

