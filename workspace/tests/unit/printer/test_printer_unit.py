import re
import pytest
from utils.print.printer import print_info, print_warn, print_error

pytestmark = [pytest.mark.printer, pytest.mark.unit]

def test_print_info_output_format(capfd):
    """測 print_info 格式（含 INFO 與時間）"""
    print_info("這是 info")
    out, _ = capfd.readouterr()
    assert "INFO" in out
    assert re.search(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] INFO", out)
    assert "這是 info" in out

@pytest.mark.parametrize("func,level,color", [
    (print_info, "INFO", "\033[92m"),
    (print_warn, "WARN", "\033[93m"),
    (print_error, "ERROR", "\033[91m"),
])
def test_print_output_format_and_color(capfd, func, level, color):
    """測三種 print function 的格式與色碼"""
    msg = f"測試 {level}"
    func(msg)
    out, _ = capfd.readouterr()
    assert level in out
    assert color in out and "\033[0m" in out
    assert msg in out

def test_printer_special_characters(capfd):
    """測印出特殊字元與 unicode"""
    print_info("特殊字元：@#%$ 中文✅")
    out, _ = capfd.readouterr()
    assert "特殊字元" in out and "中文✅" in out
