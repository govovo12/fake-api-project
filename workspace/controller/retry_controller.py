from typing import Callable, Any, Tuple, Type
from utils.retry.retry_handler import retry_call
from controller.log_controller import retry as log_retry_attempt


def run_with_retry(
    func: Callable,
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    *args,
    **kwargs
) -> Any:
    """
    執行目標函式，遇到錯誤時自動重試，並透過 log_controller 統一紀錄 retry。
    """

    def on_retry(attempt: int, error: Exception):
        log_retry_attempt(func.__name__, attempt, error)

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
