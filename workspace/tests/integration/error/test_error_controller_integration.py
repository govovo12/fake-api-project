import pytest
from workspace.controller import error_controller
from workspace.utils.error.error_handler import APIError
from workspace.config.rules import error_codes

pytestmark = pytest.mark.error

def test_process_api_exception(monkeypatch):
    messages = []
    logs = []

    monkeypatch.setattr("workspace.controller.log_controller.error", lambda msg: logs.append(msg))
    monkeypatch.setattr("workspace.notifier.telegram_notifier.send_message", lambda msg: messages.append(msg))

    err = APIError("API call failed", status_code=503, code=error_codes.API_TIMEOUT)
    result = error_controller.process_exception(err, context="login")

    assert result["type"] == "api"
    assert result["code"] == error_codes.API_TIMEOUT
    assert "[LOGIN ERROR]" in logs[0]
    assert str(error_codes.API_TIMEOUT) in logs[0]
    assert "API call failed" in logs[0]
    assert messages[0] == logs[0]

def test_process_unknown_exception(monkeypatch):
    messages = []
    logs = []

    monkeypatch.setattr("workspace.controller.log_controller.error", lambda msg: logs.append(msg))
    monkeypatch.setattr("workspace.notifier.telegram_notifier.send_message", lambda msg: messages.append(msg))

    err = RuntimeError("Unexpected crash")
    result = error_controller.process_exception(err, context="system")

    assert result["type"] == "unknown"
    assert "[SYSTEM ERROR]" in logs[0]
    assert "Unexpected crash" in logs[0]
    assert messages[0] == logs[0]
