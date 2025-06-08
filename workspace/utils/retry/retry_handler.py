import time
from typing import Callable, Any, Tuple
from functools import wraps

# ✅ 兼容你的工具掃描系統
def tool(func):
    func.is_tool = True
    func.__tool__ = True  # 雙重標記
    return func


@tool
def retry_call(
    func: Callable,
    max_retries: int = 3,
    delay: float = 0.2,
    exceptions: Tuple[Exception] = (Exception,),
    on_retry: Callable[[int, Exception], None] = None,
    *args,
    **kwargs
) -> Any:
    """
    ✅ 工具：捕捉例外型 retry 函式（func 可能會 raise）
    - max_retries: 最多重試幾次
    - delay: 每次重試等待秒數
    - exceptions: 哪些例外會觸發 retry
    - on_retry: 每次 retry 時會呼叫（可印出 / log）
    """
    attempt = 0
    while attempt < max_retries:
        try:
            return func(*args, **kwargs)
        except exceptions as e:
            attempt += 1
            if on_retry:
                on_retry(attempt, e)
            if attempt < max_retries:
                time.sleep(delay)
            else:
                raise  # 最後一次失敗就拋出


@tool
def retry_decorator(
    max_retries: int = 3,
    delay: float = 0.2,
    exceptions: Tuple[Exception] = (Exception,),
    on_retry: Callable[[int, Exception], None] = None,
):
    """
    ✅ 裝飾器形式的 retry（支援 raise 例外型函式）
    使用方式：
    @retry_decorator(...)
    def risky_func(...):
        ...
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return retry_call(func, max_retries, delay, exceptions, on_retry, *args, **kwargs)
        return wrapper
    return decorator


@tool
def retry_tool(
    func: Callable,
    max_retries: int = 2,
    delay_sec: float = 0.2,
    retry_on: Callable[[Any], bool] = lambda result: not result[0]
) -> Callable:
    """
    ✅ 工具：針對回傳 (success, ...) 結構的模組提供 retry 機制（不捕例外）
    - func: 要包裝的目標函式，需回傳 tuple 且第一位為 bool success
    - retry_on: 若回傳值符合條件（預設是失敗），則 retry
    - 使用方式：
        safe_func = retry_tool(original_func, max_retries=2)
        success, meta = safe_func(*args, **kwargs)
    """
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            result = func(*args, **kwargs)
            if not retry_on(result):
                return result
            time.sleep(delay_sec)
        return result  # 最後一次回傳
    wrapper.is_tool = True
    wrapper.__tool__ = True
    return wrapper
