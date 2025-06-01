import pytest
from utils.callback import callback_helper

pytestmark = [pytest.mark.unit, pytest.mark.callback]

def test_run_with_callback_success():
    """成功時呼叫 on_success 並正確回傳"""
    result_flag = {}
    def dummy():
        return 42
    def success():
        result_flag['ok'] = True
    r = callback_helper.run_with_callback(dummy, on_success=success)
    assert r == 42
    assert result_flag.get('ok') is True

def test_run_with_callback_failure():
    """失敗時呼叫 on_failure 並正確傳遞異常"""
    result_flag = {}
    def will_fail():
        raise ValueError("Boom")
    def failure(e):
        result_flag['err'] = str(e)
    with pytest.raises(ValueError):
        callback_helper.run_with_callback(will_fail, on_failure=failure)
    assert result_flag.get('err') == "Boom"

def test_run_with_callback_none():
    """無 callback 也能正常回傳"""
    def pure():
        return "done"
    r = callback_helper.run_with_callback(pure)
    assert r == "done"

def test_run_with_callback_failure_no_callback():
    """失敗但沒給 on_failure，應直接 re-raise"""
    def will_fail():
        raise RuntimeError("bad")
    with pytest.raises(RuntimeError):
        callback_helper.run_with_callback(will_fail)
