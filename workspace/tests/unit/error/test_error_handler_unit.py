import pytest
from workspace.utils.error import error_handler

pytestmark = pytest.mark.error

def test_api_error_exception():
    e = error_handler.APIError("timeout error", status_code=504, code="API_TIMEOUT")
    assert isinstance(e, Exception)
    assert e.status_code == 504
    assert e.code == "API_TIMEOUT"
    assert str(e) == "timeout error"

def test_validation_error_exception():
    e = error_handler.ValidationError("bad input", code="INVALID_INPUT")
    assert isinstance(e, Exception)
    assert e.code == "INVALID_INPUT"
    assert str(e) == "bad input"

def test_handle_api_error():
    e = error_handler.APIError("api fail", status_code=503, code="API_FAIL")
    res = error_handler.handle_exception(e)
    assert res == {
        "type": "api",
        "code": "API_FAIL",
        "status_code": 503,
        "msg": "api fail"
    }

def test_handle_validation_error():
    e = error_handler.ValidationError("格式不符", code="INPUT_ERR")
    res = error_handler.handle_exception(e)
    assert res == {
        "type": "validation",
        "code": "INPUT_ERR",
        "msg": "格式不符"
    }

def test_handle_unknown_error():
    e = RuntimeError("不明錯誤")
    res = error_handler.handle_exception(e)
    assert res == {
        "type": "unknown",
        "msg": "不明錯誤"
    }
