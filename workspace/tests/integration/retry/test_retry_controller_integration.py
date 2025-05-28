import pytest
from controller import retry_controller

pytestmark = [pytest.mark.integration, pytest.mark.retry]


def test_retry_controller_triggers_log_on_fail_then_succeed(capsys):
    state = {"count": 0}

    def flaky_func():
        state["count"] += 1
        if state["count"] < 3:
            raise ValueError("Temporary failure")
        return "Success"

    result = retry_controller.run_with_retry(flaky_func, max_retries=5, delay=0)

    # 驗證回傳結果正確
    assert result == "Success"

    # 驗證觸發 log 次數與內容
    captured = capsys.readouterr().out
    assert "[Retry]" in captured
    assert "flaky_func 第 1 次嘗試失敗" in captured
    assert "flaky_func 第 2 次嘗試失敗" in captured
    assert "Temporary failure" in captured


def test_retry_controller_raises_on_exceed():
    def always_fail():
        raise RuntimeError("Fatal")

    with pytest.raises(RuntimeError):
        retry_controller.run_with_retry(always_fail, max_retries=2, delay=0)
