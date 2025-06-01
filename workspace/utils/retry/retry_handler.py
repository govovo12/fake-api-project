import time
from typing import Callable, Any, Tuple, Type, Optional

def tool(func):
    """自製工具標記（供自動掃描工具表用）"""
    func.is_tool = True
    return func

@tool
def retry_call(
    func: Callable,
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[int, Exception], None]] = None,
    *args,
    **kwargs
) -> Any:
    """
    [TOOL] 通用 retry 函式。可重試任意函數，支援延遲、倍增、指定例外、重試 callback。
    - func: 要重試的 function
    - max_retries: 最大重試次數（含首次呼叫）
    - delay: 初始等待秒數
    - backoff: 每次失敗等待秒數倍增（1.0 = 固定等待）
    - exceptions: 哪些例外類型要重試
    - on_retry: 每次 retry 前的 callback (attempt, error)
    - *args, **kwargs: 傳給 func 的參數
    :return: 執行結果或最後 raise
    """
    current_delay = delay
    for attempt in range(1, max_retries + 1):
        try:
            return func(*args, **kwargs)
        except exceptions as e:
            if attempt == max_retries:
                raise
            if on_retry:
                on_retry(attempt, e)
            time.sleep(current_delay)
            current_delay *= backoff

@tool
def retry_decorator(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[int, Exception], None]] = None
) -> Callable:
    """
    [TOOL] Retry 裝飾器。加在 function 上，讓其自動支援失敗重試。
    - max_retries: 最大重試次數
    - delay: 初始等待秒數
    - backoff: 每次失敗等待秒數倍增
    - exceptions: 哪些 Exception 觸發 retry
    - on_retry: 每次 retry 時的 callback (attempt, error)
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        raise
                    if on_retry:
                        on_retry(attempt, e)
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator
