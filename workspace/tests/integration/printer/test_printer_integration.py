# workspace/tests/integration/printer/test_printer_integration.py

import uuid
import pytest
from controller.log_controller import info, warn, error

pytestmark = [pytest.mark.printer, pytest.mark.integration]

def test_info_log_through_controller(capfd):
    msg = f"整合 info 測試 {uuid.uuid4()}"
    info(msg)
    out, _ = capfd.readouterr()
    assert "INFO" in out and msg in out
    assert "\033[92m" in out

def test_warn_log_through_controller(capfd):
    msg = f"整合 warn 測試 {uuid.uuid4()}"
    warn(msg)
    out, _ = capfd.readouterr()
    assert "WARN" in out and msg in out
    assert "\033[93m" in out

def test_error_log_through_controller_with_code(capfd):
    msg = f"整合 error 測試 {uuid.uuid4()}"
    error(msg, code="E_CTRL")
    out, _ = capfd.readouterr()
    assert "ERROR" in out and msg in out and "E_CTRL" in out
    assert "\033[91m" in out

def test_multiple_log_entries_output(capfd):
    for i in range(3):
        warn(f"整合多筆輸出 {i}")
    out, _ = capfd.readouterr()
    assert out.count("WARN") == 3
