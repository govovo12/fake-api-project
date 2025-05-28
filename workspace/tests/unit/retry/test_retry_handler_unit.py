import pytest
import time
from utils.retry.retry_handler import retry_call

pytestmark = [pytest.mark.unit]

class CustomError(Exception):
    pass


def test_retry_success_on_first_attempt():
    def always_succeed():
        return "ok"

    result = retry_call(always_succeed)
    assert result == "ok"


def test_retry_until_success(monkeypatch):
    calls = []

    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise ValueError("fail")
        return "ok"

    result = retry_call(flaky, max_retries=5, delay=0)
    assert result == "ok"
    assert len(calls) == 3


def test_retry_exceeds_max_retries():
    def always_fail():
        raise RuntimeError("nope")

    with pytest.raises(RuntimeError):
        retry_call(always_fail, max_retries=2, delay=0)


def test_retry_with_backoff(monkeypatch):
    delays = []

    def mock_sleep(seconds):
        delays.append(seconds)

    monkeypatch.setattr(time, "sleep", mock_sleep)

    call_count = {"n": 0}

    def failing_func():
        call_count["n"] += 1
        raise CustomError("fail")

    with pytest.raises(CustomError):
        retry_call(failing_func, max_retries=3, delay=1.0, backoff=2.0, exceptions=(CustomError,))

    assert delays == [1.0, 2.0]


def test_retry_callback_triggered():
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
        exceptions=(ValueError,),
        on_retry=on_retry
    )

    assert result == "ok"
    assert attempts_logged == [(1, "fail"), (2, "fail")]
