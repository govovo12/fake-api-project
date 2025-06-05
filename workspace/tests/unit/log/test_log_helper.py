import pytest
from workspace.utils.logger.log_helper import log_step

pytestmark = [pytest.mark.unit, pytest.mark.log]

def test_log_step_success(capfd):
    """
    測試 log_step 輸出成功訊息
    """
    log_step("測試步驟", 0)
    out, err = capfd.readouterr()
    assert "【測試步驟】成功" in out
    assert "狀態碼：0" in out
    assert "說明：" in out

def test_log_step_fail(capfd):
    """
    測試 log_step 輸出失敗訊息
    """
    log_step("測試步驟", 99999)
    out, err = capfd.readouterr()
    assert "【測試步驟】失敗" in out
    assert "狀態碼：99999" in out
    assert "說明：" in out or "未知狀態" in out

def test_log_step_custom_code(capfd):
    """
    測試 log_step 對已知錯誤碼的對應說明
    """
    from workspace.config.rules.error_codes import ERROR_CODE_MSG_MAP
    custom_code = next(iter(ERROR_CODE_MSG_MAP))
    log_step("自訂步驟", custom_code)
    out, err = capfd.readouterr()
    assert f"狀態碼：{custom_code}" in out
    assert ERROR_CODE_MSG_MAP[custom_code] in out
