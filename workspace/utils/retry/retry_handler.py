from typing import Callable, Any, Tuple, List
import time

def tool(func):
    """自製工具標記（供工具掃描系統使用）"""
    func.is_tool = True
    return func

@tool
def retry_on_code(
    func: Callable[..., Tuple[int, Any]],
    *,
    retry_codes: List[int],
    max_retries: int = 3,
    delay: float = 0.2
) -> Callable[..., Tuple[int, Any]]:
    """
    ✅ 工具：根據錯誤碼進行 retry（不捕例外）
    - func 必須回傳 (code, payload)
    - 若 code 在 retry_codes 中，則 retry
    """
    def wrapper(*args, **kwargs) -> Tuple[int, Any]:
        for attempt in range(1, max_retries + 1):
            code, payload = func(*args, **kwargs)
            if code not in retry_codes:
                return code, payload
            time.sleep(delay)
        return code, payload
    return wrapper
