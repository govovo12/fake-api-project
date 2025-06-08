# workspace/utils/logger/trace_helper.py

def print_trace(uuid: str, step: str, extra: str = ""):
    """
    印出統一格式的 UUID 流程追蹤資訊。

    Args:
        uuid (str): 此筆資料的識別碼（由主控流程產生）
        step (str): 當前執行步驟名稱
        extra (str): 額外補充說明
    """
    print(f"🔍 [TRACE] UUID={uuid}｜Step={step}｜{extra}")
