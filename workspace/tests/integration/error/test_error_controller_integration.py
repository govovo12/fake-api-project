import pytest
from workspace.controller import error_controller

pytestmark = pytest.mark.error

def test_process_api_exception(monkeypatch):
    messages = []
    logs = []

    # monkeypatch log_controller.error
    monkeypatch.setattr("workspace.controller.log_controller.error", lambda msg, code=None: logs.append((msg, code)))
    # monkeypatch TelegramNotifier.send
    monkeypatch.setattr(
        "workspace.utils.notifier.telegram_notifier.TelegramNotifier.send",
        lambda self, msg: messages.append(msg)
    )

    # 這邊模擬錯誤事件觸發
    error_controller.process_api_exception(Exception("API FAIL"))

    assert any("API FAIL" in m[0] for m in logs)
    assert any("API FAIL" in m for m in messages)

def test_process_unknown_exception(monkeypatch):
    messages = []
    logs = []

    monkeypatch.setattr("workspace.controller.log_controller.error", lambda msg, code=None: logs.append((msg, code)))
    monkeypatch.setattr(
        "workspace.utils.notifier.telegram_notifier.TelegramNotifier.send",
        lambda self, msg: messages.append(msg)
    )

    error_controller.process_unknown_exception(Exception("???"))

    assert any("???" in m[0] for m in logs)
    assert any("???" in m for m in messages)
