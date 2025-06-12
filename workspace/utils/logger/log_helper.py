from typing import Optional
from pathlib import Path
from workspace.config.rules.error_codes import ResultCode

# ✅ 工具函式標記（供 tools_table 掃描用）
def tool(func):
    """自製工具標記（供自動掃描工具表用）"""
    func.is_tool = True
    return func

@tool
def log_simple_result(code: int):
    """
    [TOOL] 印出結果格式： (code=xxx, msg=XXX)
    支援成功碼與錯誤碼。
    """
    msg = ResultCode.ERROR_MESSAGES.get(code, "未知錯誤")
    status = "✅ 成功" if ResultCode.is_success(code) else "❌ 失敗"
    print(f"[{status}] (code={code}, msg={msg})")