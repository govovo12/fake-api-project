import time
from typing import Callable, Any, Tuple

def retry_call(
    func: Callable,
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 1.0,
    exceptions: Tuple = (Exception,),
    on_retry: Callable[[int, Exception], None] = None,
    *args,
    **kwargs
) -> Any:
    """
    通用 retry 函數：執行 func，當遇到指定例外時最多重試 max_retries 次。

    :param func: 要執行的目標函數
    :param max_retries: 最大重試次數（包含第一次）
    :param delay: 初始延遲秒數
    :param backoff: 每次失敗延遲成長倍率
    :param exceptions: 要捕捉的錯誤型別（tuple）
    :param on_retry: 每次 retry 前可呼叫 callback，提供 (嘗試次數, 例外錯誤)
    :return: func 執行結果，或最終錯誤由上層處理
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