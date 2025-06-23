from typing import Callable, List, Any
import time

def tool(func):
    """自製工具標記（供工具表用）"""
    func.is_tool = True
    return func

@tool
def retry_on_code(
    func: Callable[..., Any],
    *,
    retry_codes: List[int],
    max_retries: int = 3,
    delay: float = 0.2
) -> Callable[..., Any]:
    """
    通用 retry 工具：依據錯誤碼進行重試。

    支援 func 回傳 int 或 (int, payload)，
    不混入任何業務邏輯，由呼叫端決定如何解讀回傳值。
    """
    def wrapper(*args, **kwargs):
        for _ in range(max_retries):
            result = func(*args, **kwargs)
            code = result[0] if isinstance(result, tuple) else result
            if code not in retry_codes:
                return result
            time.sleep(delay)
        return result
    return wrapper
