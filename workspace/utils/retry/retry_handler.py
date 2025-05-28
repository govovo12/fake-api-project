import time
from typing import Callable, Any, Tuple, Type


def retry_call(
    func: Callable,
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Callable[[int, Exception], None] = None,
    *args,
    **kwargs
) -> Any:
    """
    通用 retry 函數，傳入任意函式與參數，遇到指定例外時重試。

    :param func: 要執行的目標函式
    :param max_retries: 最大重試次數（包含第一次）
    :param delay: 初始延遲秒數
    :param backoff: 延遲成長倍率
    :param exceptions: 要捕捉的例外型別
    :param on_retry: 每次 retry 前執行的 callback，參數為 (當前重試次數, 例外)
    :return: 函式執行結果，或最終錯誤由上層處理
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


def retry_decorator(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Callable[[int, Exception], None] = None
):
    """
    裝飾器版本 retry，可裝飾任意函式並套用 retry 行為。
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            return retry_call(
                func,
                max_retries=max_retries,
                delay=delay,
                backoff=backoff,
                exceptions=exceptions,
                on_retry=on_retry,
                *args,
                **kwargs
            )
        return wrapper
    return decorator
