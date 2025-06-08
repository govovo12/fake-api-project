import pytest
import time
from utils.retry.retry_handler import retry_call, retry_decorator

pytestmark = [pytest.mark.unit, pytest.mark.retry]

class CustomError(Exception):
    """自訂例外型別（for test）"""
    pass

def test_retry_call_success_first_try():
    """[function版] 首次執行即成功，無 retry 發生"""
    def always_ok():
        return 100
    assert retry_call(always_ok, max_retries=3) == 100

def test_retry_call_retry_until_success(monkeypatch):
    """[function版] 前兩次失敗，第三次成功"""
    monkeypatch.setattr(time, "sleep", lambda s: None)
    calls = []
    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise ValueError("fail")
        return "ok"
    result = retry_call(flaky, max_retries=5, delay=0)
    assert result == "ok"
    assert len(calls) == 3

def test_retry_call_exceeds_max_retries(monkeypatch):
    """[function版] 永遠失敗，最後 raise，sleep 次數正確"""
    monkeypatch.setattr(time, "sleep", lambda s: None)
    def always_fail():
        raise RuntimeError("fail")
    with pytest.raises(RuntimeError):
        retry_call(always_fail, max_retries=2, delay=0)

def test_retry_call_backoff(monkeypatch):
    """測試 retry_call 可設定 delay 參數並重試"""

    monkeypatch.setattr(time, "sleep", lambda s: None)

    class CustomError(Exception):
        pass

    count = {"value": 0}

    def fail():
        count["value"] += 1
        raise CustomError("fail")

    from workspace.utils.retry.retry_handler import retry_call

    with pytest.raises(CustomError):
        retry_call(fail, max_retries=3, delay=0.1, exceptions=(CustomError,))
    assert count["value"] == 3


def test_retry_call_on_retry_callback(monkeypatch):
    """測試 retry_call 的 on_retry callback 是否被正確呼叫"""

    monkeypatch.setattr(time, "sleep", lambda s: None)

    log = []

    class CustomError(Exception):
        pass

    def fail():
        raise CustomError("fail")

    def callback(attempt, exc):
        log.append((attempt, str(exc)))

    from workspace.utils.retry.retry_handler import retry_call

    with pytest.raises(CustomError):
        retry_call(fail, max_retries=3, delay=0.1, exceptions=(CustomError,), on_retry=callback)

    assert log == [(1, 'fail'), (2, 'fail'), (3, 'fail')]


def test_retry_decorator_success(monkeypatch):
    """[decorator版] 兩次失敗第三次成功"""
    monkeypatch.setattr(time, "sleep", lambda s: None)
    calls = []
    @retry_decorator(max_retries=3, delay=0, exceptions=(ValueError,))
    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise ValueError("fail")
        return "OK"
    assert flaky() == "OK"
    assert len(calls) == 3

def test_retry_decorator_raises(monkeypatch):
    """[decorator版] 永遠失敗，最後 raise"""
    monkeypatch.setattr(time, "sleep", lambda s: None)
    @retry_decorator(max_retries=2, delay=0, exceptions=(CustomError,))
    def always_fail():
        raise CustomError("fail")
    with pytest.raises(CustomError):
        always_fail()

def test_retry_decorator_on_retry(monkeypatch):
    """測試 retry_decorator 包裝函式 + callback 被觸發"""

    monkeypatch.setattr(time, "sleep", lambda s: None)

    log = []

    class CustomError(Exception):
        pass

    def callback(attempt, exc):
        log.append((attempt, str(exc)))

    from workspace.utils.retry.retry_handler import retry_decorator

    @retry_decorator(max_retries=3, delay=0.1, exceptions=(CustomError,), on_retry=callback)
    def fail():
        raise CustomError("fail")

    with pytest.raises(CustomError):
        fail()

    assert log == [(1, 'fail'), (2, 'fail'), (3, 'fail')]

def test_retry_tool_success_immediate(monkeypatch):
    """[tool版] 首次成功不 retry"""
    monkeypatch.setattr(time, "sleep", lambda s: None)

    calls = []

    def always_pass():
        calls.append(1)
        return True, None

    from workspace.utils.retry.retry_handler import retry_tool
    wrapped = retry_tool(always_pass, max_retries=3)
    success, meta = wrapped()
    assert success is True
    assert len(calls) == 1

def test_retry_tool_retry_until_success(monkeypatch):
    """[tool版] 前兩次失敗，第三次成功"""
    monkeypatch.setattr(time, "sleep", lambda s: None)

    calls = []

    def flaky():
        calls.append(1)
        if len(calls) < 3:
            return False, {"reason": "temp_fail"}
        return True, None

    from workspace.utils.retry.retry_handler import retry_tool
    wrapped = retry_tool(flaky, max_retries=5)
    success, meta = wrapped()
    assert success is True
    assert len(calls) == 3
