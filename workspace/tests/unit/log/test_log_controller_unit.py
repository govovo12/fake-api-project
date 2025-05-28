import pytest
from config.paths import LOG_PATH
from controller.log_controller import info, warn, error
from pathlib import Path
import uuid

pytestmark = [pytest.mark.log, pytest.mark.unit]


@pytest.fixture(autouse=True)
def clear_log_file():
    if LOG_PATH.exists():
        LOG_PATH.unlink()
    yield
    if LOG_PATH.exists():
        LOG_PATH.unlink()


def read_log():
    return LOG_PATH.read_text(encoding="utf-8")


def test_log_info_written():
    test_message = f"info test {uuid.uuid4()}"
    info(test_message)
    log = read_log()
    assert f"[INFO] {test_message}" in log


def test_log_warn_written():
    test_message = f"warn test {uuid.uuid4()}"
    warn(test_message)
    log = read_log()
    assert f"[WARN] {test_message}" in log


def test_log_error_with_code():
    test_message = f"error test {uuid.uuid4()}"
    error(test_message, code="E_LOG_TEST")
    log = read_log()
    assert "[ERROR] [E_LOG_TEST]" in log
    assert test_message in log


def test_log_special_characters():
    test_message = "特殊字元測試 @!#$% 中文✅"
    info(test_message)
    log = read_log()
    assert test_message in log


def test_log_multiple_entries():
    messages = [f"entry {i}" for i in range(3)]
    for msg in messages:
        warn(msg)
    log = read_log()
    for msg in messages:
        assert msg in log
