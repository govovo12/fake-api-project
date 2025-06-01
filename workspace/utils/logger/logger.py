def tool(func):
    """自製工具標記（供自動掃描工具表用）"""
    func.is_tool = True
    return func

@tool
def format_log_message(level: str, message: str, timestamp: str) -> str:
    """
    [TOOL] 格式化 log 字串，標準格式：[timestamp] [level] message
    """
    return f"[{timestamp}] [{level}] {message}"
