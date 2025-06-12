from typing import Callable

# ✅ 工具函式標記（供工具表掃描用）
def tool(func: Callable) -> Callable:
    """工具函式裝飾器：標記為工具模組用函式"""
    func.is_tool = True
    return func

@tool
def print_trace(step: str) -> None:
    """
    [TOOL] 印出 trace 訊息，標示當前步驟或 UUID
    - 通常用於子控制器流程追蹤
    - 輸出格式：[TRACE] {step}
    """
    print(f"[TRACE] {step}")
