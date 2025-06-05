import pytest
from workspace.config.rules import error_codes
from workspace.utils.error import error_handler

pytestmark = [pytest.mark.infra, pytest.mark.errorcode]


# ✅ 結構性測試：錯誤碼檢查
def test_all_error_codes_are_int():
    """所有錯誤碼應為 int，且為非負整數"""
    for attr in dir(error_codes.ResultCode):
        if attr.startswith("__"):
            continue
        value = getattr(error_codes.ResultCode, attr)
        assert isinstance(value, int), f"{attr} is not an int"
        assert value >= 0, f"{attr} has negative value {value}"


def test_error_code_names_are_uppercase():
    """錯誤碼命名應為全大寫（維護一致性）"""
    for attr in dir(error_codes.ResultCode):
        if attr.startswith("__"):
            continue
        assert attr.isupper(), f"{attr} is not uppercase"


def test_error_codes_are_unique():
    """錯誤碼數值應唯一，避免重複"""
    values = []
    for attr in dir(error_codes.ResultCode):
        if attr.startswith("__"):
            continue
        val = getattr(error_codes.ResultCode, attr)
        values.append(val)
    duplicates = {v for v in values if values.count(v) > 1}
    assert not duplicates, f"Duplicate error code values found: {duplicates}"


# ✅ 行為性測試：錯誤處理轉換
def test_handle_api_error():
    e = error_handler.APIError("timeout", status_code=504, code=error_codes.ResultCode.API_TIMEOUT)
    result = error_handler.handle_exception(e)
    assert result["type"] == "api"
    assert result["code"] == error_codes.ResultCode.API_TIMEOUT
    assert result["status_code"] == 504
    assert result["msg"] == "timeout"


def test_handle_validation_error():
    e = error_handler.ValidationError("name required", code="NAME_REQUIRED")
    result = error_handler.handle_exception(e)
    assert result["type"] == "validation"
    assert result["code"] == "NAME_REQUIRED"
    assert result["msg"] == "name required"


def test_handle_unknown_error():
    e = RuntimeError("something went wrong")
    result = error_handler.handle_exception(e)
    assert result["type"] == "unknown"
    assert result["msg"] == "something went wrong"
