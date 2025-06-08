import pytest
from workspace.config.rules import error_codes
from workspace.utils.error import error_handler

pytestmark = [pytest.mark.infra, pytest.mark.errorcode]

# ✅ 結構性測試：ResultCode 的設計是否正確

def test_all_error_codes_are_int():
    """所有錯誤碼應為 int，且非負"""
    for attr in dir(error_codes.ResultCode):
        if attr.startswith("__"):
            continue
        val = getattr(error_codes.ResultCode, attr)
        assert isinstance(val, int), f"{attr} is not int"
        assert val >= 0, f"{attr} is negative"


def test_error_code_names_are_uppercase():
    """錯誤碼名稱需全大寫（維持一致性）"""
    for attr in dir(error_codes.ResultCode):
        if attr.startswith("__"):
            continue
        assert attr.isupper(), f"{attr} is not uppercase"


def test_error_codes_are_unique():
    """錯誤碼 value 不可重複"""
    values = []
    for attr in dir(error_codes.ResultCode):
        if attr.startswith("__"):
            continue
        values.append(getattr(error_codes.ResultCode, attr))
    duplicates = {v for v in values if values.count(v) > 1}
    assert not duplicates, f"Duplicate error codes: {duplicates}"


# ✅ 功能性測試：error_handler 處理錯誤格式是否正確

def test_handle_api_error_with_any_int_code():
    e = error_handler.APIError("timeout", status_code=504, code=8888)
    result = error_handler.handle_exception(e)
    assert result["type"] == "api"
    assert result["msg"] == "timeout"
    assert result["status_code"] == 504
    assert result["code"] == 8888


def test_handle_api_error_with_default_code():
    e = error_handler.APIError("fallback error")
    result = error_handler.handle_exception(e)
    assert result["type"] == "api"
    assert result["msg"] == "fallback error"
    assert isinstance(result["code"], int)


def test_handle_validation_error():
    e = error_handler.ValidationError("email required", code="EMAIL_REQUIRED")
    result = error_handler.handle_exception(e)
    assert result["type"] == "validation"
    assert result["code"] == "EMAIL_REQUIRED"
    assert result["msg"] == "email required"


def test_handle_unknown_error():
    e = RuntimeError("unexpected failure")
    result = error_handler.handle_exception(e)
    assert result["type"] == "unknown"
    assert result["msg"] == "unexpected failure"
