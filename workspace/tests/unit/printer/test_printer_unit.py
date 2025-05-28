# workspace/tests/unit/printer/test_printer_unit.py

import re
import pytest
from utils.print.printer import print_info, print_warn, print_error

pytestmark = [pytest.mark.printer, pytest.mark.unit]

def test_print_info_output_format(capfd):
    print_info("這是 info")
    out, _ = capfd.readouterr()
    assert "INFO" in out
    assert re.search(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] INFO", out)
    assert "這是 info" in out

def test_print_warn_output_format(capfd):
    print_warn("這是 warn")
    out, _ = capfd.readouterr()
    assert "WARN" in out
    assert re.search(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] WARN", out)
    assert "這是 warn" in out

def test_print_error_output_format(capfd):
    print_error("這是 error")
    out, _ = capfd.readouterr()
    assert "ERROR" in out
    assert re.search(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] ERROR", out)
    assert "這是 error" in out

def test_print_info_contains_color_code(capfd):
    print_info("顏色測試 info")
    out, _ = capfd.readouterr()
    assert "\033[92m" in out and "\033[0m" in out


def test_print_warn_contains_color_code(capfd):
    print_warn("顏色測試 warn")
    out, _ = capfd.readouterr()
    assert "\033[93m" in out and "\033[0m" in out


def test_print_error_contains_color_code(capfd):
    print_error("顏色測試 error")
    out, _ = capfd.readouterr()
    assert "\033[91m" in out and "\033[0m" in out


def test_printer_special_characters(capfd):
    print_info("特殊字元：@#%$ 中文✅")
    out, _ = capfd.readouterr()
    assert "特殊字元" in out and "中文✅" in out
