# workspace/utils/logger/log_helper.py

from workspace.config.rules.error_codes import ERROR_CODE_MSG_MAP
from workspace.utils.print.printer import print_info, print_error

def tool(func):
    """自製工具標記（供自動掃描工具表用）"""
    func.is_tool = True
    return func

@tool
def log_step(step: str, code: int):
    """
    根據狀態碼自動印出【步驟】成功/失敗訊息與錯誤說明

    Args:
        step (str): 步驟或行為名稱
        code (int): 狀態/錯誤碼
    """
    msg = ERROR_CODE_MSG_MAP.get(code, "未知狀態")
    if code == 0:
        print_info(f"【{step}】成功｜狀態碼：{code}｜說明：{msg}")
    else:
        print_error(f"【{step}】失敗｜狀態碼：{code}｜說明：{msg}")
