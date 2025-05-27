import re
from utils.logger.logger import log_info, log_error
from config.rules.error_codes import ACCOUNT_GEN_FAIL
import pytest

pytestmark = [pytest.mark.account_generator, pytest.mark.unit]


pytestmark = [pytest.mark.account_generator, pytest.mark.unit]

def test_log_info_output(capfd):
    log_info("測試 info log")
    out, _ = capfd.readouterr()
    assert "INFO" in out
    assert "測試 info log" in out

def test_log_error_with_code(capfd):
    log_error("錯誤發生", code=ACCOUNT_GEN_FAIL)
    out, _ = capfd.readouterr()
    assert "ERROR" in out
    assert "錯誤發生" in out
    assert "1001" in out  # 錯誤碼
