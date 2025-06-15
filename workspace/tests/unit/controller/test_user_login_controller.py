import pytest
from importlib import reload
import workspace.controller.user_login_controller as controller
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.login, pytest.mark.controller]


def test_login_controller_success_first_try(monkeypatch):
    """✅ 第一次登入成功，應直接回傳成功碼與 token"""
    monkeypatch.setattr(
        "workspace.modules.login.login_user.login_user",
        lambda *_: (ResultCode.LOGIN_TASK_SUCCESS, "tokenABC")
    )
    reload(controller)

    code, token = controller.login_and_report(
        cred={"username": "user", "password": "pass"},
        headers={"Content-Type": "application/json"}
    )

    assert code == ResultCode.LOGIN_TASK_SUCCESS
    assert token == "tokenABC"


def test_login_controller_api_failed_no_retry(monkeypatch):
    """❌ 回傳非可重試錯誤（如帳密錯），不應 retry"""
    count = {"calls": 0}

    def mock_login(*args, **kwargs):
        count["calls"] += 1
        return ResultCode.LOGIN_API_FAILED, None

    monkeypatch.setattr(
        "workspace.modules.login.login_user.login_user",
        mock_login
    )
    reload(controller)

    code, token = controller.login_and_report(
        cred={"username": "user", "password": "wrong"},
        headers={"Content-Type": "application/json"}
    )

    assert code == ResultCode.LOGIN_API_FAILED
    assert token is None
    assert count["calls"] == 1


def test_login_controller_retry_then_success(monkeypatch):
    """🔁 第一次 LOGIN_EXCEPTION，第二次成功"""
    responses = [
        (ResultCode.LOGIN_EXCEPTION, None),
        (ResultCode.LOGIN_TASK_SUCCESS, "tokenXYZ")
    ]

    monkeypatch.setattr(
        "workspace.modules.login.login_user.login_user",
        lambda *_: responses.pop(0)
    )
    reload(controller)

    code, token = controller.login_and_report(
        cred={"username": "user", "password": "retry"},
        headers={"Content-Type": "application/json"}
    )

    assert code == ResultCode.LOGIN_TASK_SUCCESS
    assert token == "tokenXYZ"


def test_login_controller_all_retries_failed(monkeypatch):
    """💥 模擬連續失敗，應重試 3 次然後放棄"""
    count = {"calls": 0}

    def always_fail(*args, **kwargs):
        count["calls"] += 1
        return ResultCode.LOGIN_EXCEPTION, None

    monkeypatch.setattr(
        "workspace.modules.login.login_user.login_user",
        always_fail
    )
    reload(controller)

    code, token = controller.login_and_report(
        cred={"username": "user", "password": "fail"},
        headers={"Content-Type": "application/json"}
    )

    assert code == ResultCode.LOGIN_EXCEPTION
    assert token is None
    assert count["calls"] == 3
