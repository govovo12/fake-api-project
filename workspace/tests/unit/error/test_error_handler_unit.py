import pytest
from workspace.utils.error import error_handler

pytestmark = [pytest.mark.unit, pytest.mark.error]

def test_api_error_exception_full_attrs():
    """APIError 可正確帶入 message、status_code、code，__str__ 正確"""
    e = error_handler.APIError("timeout error", status_code=504, code=9001)
    assert isinstance(e, Exception)
    assert e.status_code == 504
    assert e.code == 9001
    assert str(e) == "timeout error"

def test_api_error_default_code():
    """APIError 未傳 code 時，預設應為 error_codes.API_TIMEOUT"""
    e = error_handler.APIError("x")
    # 預設 code 應為 int，且與 error_codes.API_TIMEOUT 相同
    from workspace.config.rules import error_codes
    assert e.code == error_codes.API_TIMEOUT

def test_validation_error_exception():
    """ValidationError 可正確帶入 message 與 code，__str__ 正確"""
    e = error_handler.ValidationError("bad input", code="INVALID_INPUT")
    assert isinstance(e, Exception)
    assert e.code == "INVALID_INPUT"
    assert str(e) == "bad input"

def test_validation_error_default_code():
    """ValidationError 未傳 code 預設為 VALIDATION_ERROR"""
    e = error_handler.ValidationError("missing field")
    assert e.code == "VALIDATION_ERROR"

def test_handle_api_error():
    """handle_exception 對 APIError 應完整正確解析"""
    e = error_handler.APIError("api fail", status_code=503, code=2001)
    res = error_handler.handle_exception(e)
    assert res == {
        "type": "api",
        "code": 2001,
        "status_code": 503,
        "msg": "api fail"
    }

def test_handle_validation_error():
    """handle_exception 對 ValidationError 應正確解析"""
    e = error_handler.ValidationError("格式不符", code="INPUT_ERR")
    res = error_handler.handle_exception(e)
    assert res == {
        "type": "validation",
        "code": "INPUT_ERR",
        "msg": "格式不符"
    }

def test_handle_unknown_error():
    """handle_exception 對未知 Exception 應正確解析"""
    e = RuntimeError("不明錯誤")
    res = error_handler.handle_exception(e)
    assert res == {
        "type": "unknown",
        "msg": "不明錯誤"
    }

def test_handle_api_error_missing_optional():
    """APIError 部分參數遺漏（如沒 status_code），handle_exception 仍可正確輸出"""
    e = error_handler.APIError("只給 message", code=1001)
    res = error_handler.handle_exception(e)
    assert res["type"] == "api"
    assert res["code"] == 1001
    assert res["status_code"] is None
    assert res["msg"] == "只給 message"

def test_handle_exception_with_log(monkeypatch):
    """傳入 log callback 時，handle_exception 應正確呼叫 log"""
    logs = []
    def fake_log(msg):
        logs.append(msg)
    e = error_handler.APIError("api err", status_code=400, code=2002)
    res = error_handler.handle_exception(e, log=fake_log)
    assert any("APIError" in m and "api err" in m for m in logs)
    assert res["type"] == "api"
