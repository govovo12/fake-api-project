import pytest

# 測試標記：unit 單元測試 + log 類別
pytestmark = [pytest.mark.unit, pytest.mark.log]

# 測試目標模組
from workspace.utils.logger.trace_helper import print_trace



def test_print_trace_basic(capfd):
    """
    測試 print_trace 基本輸出是否正確包含 step
    """
    print_trace("STEP 1")
    out, err = capfd.readouterr()
    assert "[TRACE] STEP 1" in out


def test_print_trace_with_note(capfd):
    """
    測試 print_trace 搭配 note 的輸出格式是否正確
    """
    print_trace("STEP 2", "建立產品")
    out, err = capfd.readouterr()
    assert "[TRACE] STEP 2 - 建立產品" in out

