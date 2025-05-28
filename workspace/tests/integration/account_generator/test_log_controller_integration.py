import pytest
from controller.log_controller import info, error
from config.paths import LOG_PATH
import uuid

pytestmark = [pytest.mark.log, pytest.mark.integration]


@pytest.fixture(autouse=True)
def clear_log_file():
    if LOG_PATH.exists():
        LOG_PATH.unlink()
    yield
    if LOG_PATH.exists():
        LOG_PATH.unlink()


def test_info_log_writes_to_file():
    message = f"[整合測試] info log {uuid.uuid4()}"
    info(message)
    content = LOG_PATH.read_text(encoding="utf-8")
    assert f"[INFO] {message}" in content


def test_error_log_with_code_written():
    message = f"[整合測試] error log {uuid.uuid4()}"
    error(message, code="INTE_ERR")
    content = LOG_PATH.read_text(encoding="utf-8")
    assert "[ERROR] [INTE_ERR]" in content
    assert message in content
