from typing import Optional

from workspace.config.rules.error_codes import SUCCESS_CODES, ERROR_MESSAGES


def is_success_code(code: int) -> bool:
    """
    判斷是否為成功碼（根據 SUCCESS_CODES）
    """
    return code in SUCCESS_CODES


def log_step(code: int, step: str, meta: Optional[dict] = None):
    """
    印出每個步驟的執行結果（成功 / 失敗）
    - 若非成功碼會一併顯示錯誤訊息與附加資訊
    """
    if is_success_code(code):
        print(f"[✅ 成功] 步驟：{step}")
    else:
        message = ERROR_MESSAGES.get(code, "未知錯誤")
        print(f"[❌ 失敗] 步驟：{step}")
        print(f"   ⤷ 錯誤碼：{code} - {message}")
        if meta:
            print(f"   ⤷ 附加資訊：{meta}")
