import pytest
from workspace.utils.callback import callback_helper

@pytest.mark.callback
def test_run_with_callback_success():
    result_flag = {}

    def dummy():
        return 42

    def success():
        result_flag['ok'] = True

    r = callback_helper.run_with_callback(dummy, on_success=success)
    assert r == 42
    assert result_flag.get('ok') is True

@pytest.mark.callback
def test_run_with_callback_failure():
    result_flag = {}

    def will_fail():
        raise ValueError("Boom")

    def failure(e):
        result_flag['err'] = str(e)

    with pytest.raises(ValueError):
        callback_helper.run_with_callback(will_fail, on_failure=failure)

    assert result_flag.get('err') == "Boom"

@pytest.mark.callback
def test_run_with_callback_none():
    def pure():
        return "done"

    r = callback_helper.run_with_callback(pure)
    assert r == "done"
