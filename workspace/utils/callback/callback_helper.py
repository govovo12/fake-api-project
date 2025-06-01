from typing import Callable, Any

def tool(func):
    """自製工具標記裝飾器，供自動掃描用"""
    func.is_tool = True
    return func

@tool
def run_with_callback(
    target_fn: Callable[[], Any],
    on_success: Callable[[], None] = None,
    on_failure: Callable[[Exception], None] = None
) -> Any:
    """
    執行目標函式，若成功可觸發成功回呼，失敗可觸發錯誤回呼
    - target_fn: 要執行的主體邏輯，無參數
    - on_success: 成功時觸發的回呼，無參數
    - on_failure: 失敗時觸發的回呼，接收 Exception
    """
    try:
        result = target_fn()
        if on_success:
            on_success()
        return result
    except Exception as e:
        if on_failure:
            on_failure(e)
        raise
