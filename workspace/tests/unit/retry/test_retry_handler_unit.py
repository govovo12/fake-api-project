
# workspace/tests/unit/retry/test_retry_handler_unit.py

import pytest
import time
from utils.retry.retry_handler import retry_call
from utils.mock.mock_helper import mock_function

pytestmark = [pytest.mark.unit, pytest.mark.retry]

class CustomError(Exception):
    pass


def test_retry_success_on_first_attempt():
    def always_succeed():
        return "ok"

    result = retry_call(always_succeed)
    assert result == "ok"


def test_retry_until_success(monkeypatch):
    # stub time.sleep 為 noop
    sleep_stub = mock_function()
    monkeypatch.setattr("time.sleep", sleep_stub)

    calls = []
    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise ValueError("fail")
        return "ok"

    result = retry_call(flaky, max_retries=5, delay=0)
    assert result == "ok"
    assert len(calls) == 3
    # 應呼叫 sleep 2 次
    assert sleep_stub.call_count == 2


def test_retry_exceeds_max_retries(monkeypatch):
    # stub time.sleep 為 noop
    sleep_stub = mock_function()
    monkeypatch.setattr("time.sleep", sleep_stub)

    def always_fail():
        raise RuntimeError("nope")

    with pytest.raises(RuntimeError):
        retry_call(always_fail, max_retries=2, delay=0)
    # exceed retries: implementation sleeps max_retries-1 times
    assert sleep_stub.call_count == 1


def test_retry_with_backoff(monkeypatch):
    # stub time.sleep 並記錄參數
    sleep_stub = mock_function()
    monkeypatch.setattr("time.sleep", sleep_stub)

    call_count = {"n": 0}
    def failing_func():
        call_count["n"] += 1
        raise CustomError("fail")

    with pytest.raises(CustomError):
        retry_call(
            failing_func,
            max_retries=3,
            delay=1.0,
            backoff=2.0,
            exceptions=(CustomError,)
        )
    # 應依次呼叫 sleep(1.0) 和 sleep(2.0)
    call_args = [args[0] for args, _ in sleep_stub.call_args_list]
    assert call_args == [1.0, 2.0]


def test_retry_callback_triggered(monkeypatch):
    # stub time.sleep 為 noop
    sleep_stub = mock_function()
    monkeypatch.setattr("time.sleep", sleep_stub)

    attempts_logged = []
    def fail_then_succeed():
        if len(attempts_logged) < 2:
            raise ValueError("fail")
        return "ok"

    def on_retry(attempt, error):
        attempts_logged.append((attempt, str(error)))

    result = retry_call(
        fail_then_succeed,
        max_retries=5,
        delay=0,
        backoff=1.0,
        exceptions=(ValueError,),
        on_retry=on_retry
    )
    assert result == "ok"
    assert attempts_logged == [(1, "fail"), (2, "fail")]
    assert sleep_stub.call_count == 2

