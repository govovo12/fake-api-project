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
    """[function版] backoff 倍增 sleep（驗證 sleep 時間）"""
    sleeps = []
    monkeypatch.setattr(time, "sleep", lambda s: sleeps.append(s))
    def fail():
        raise CustomError("fail")
    with pytest.raises(CustomError):
        retry_call(fail, max_retries=3, delay=1.0, backoff=2.0, exceptions=(CustomError,))
    assert sleeps == [1.0, 2.0]

def test_retry_call_on_retry_callback(monkeypatch):
    """[function版] on_retry callback 被正確呼叫"""
    monkeypatch.setattr(time, "sleep", lambda s: None)
    log = []
    def fail():
        raise ValueError("fail")
    def on_retry(attempt, error):
        log.append((attempt, str(error)))
    with pytest.raises(ValueError):
        retry_call(fail, max_retries=3, delay=0, on_retry=on_retry, exceptions=(ValueError,))
    assert log == [(1, "fail"), (2, "fail")]

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
    """[decorator版] on_retry callback 會被呼叫"""
    monkeypatch.setattr(time, "sleep", lambda s: None)
    log = []
    def cb(attempt, error):
        log.append((attempt, str(error)))
    @retry_decorator(max_retries=3, delay=0, exceptions=(CustomError,), on_retry=cb)
    def fail():
        raise CustomError("fail")
    with pytest.raises(CustomError):
        fail()
    assert log == [(1, "fail"), (2, "fail")]
