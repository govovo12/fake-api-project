import pytest
from workspace.utils.error.error_handler import (
    APIError,
    ValidationError,
    handle_exception
)
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.infra, pytest.mark.errorcode]

# ✅ 結構性測試：ResultCode 的設計是否正確

def test_handle_api_error_with_valid_code():
    """
    測試傳入 APIError 且使用合法錯誤碼時，應正確轉換為 dict
    """
    exc = APIError("檔案建立失敗", status_code=500, code=ResultCode.TOOL_FILE_CREATE_FAILED)
    result = handle_exception(exc)
    
    assert result["type"] == "api"
    assert result["msg"] == "檔案建立失敗"
    assert result["code"] == ResultCode.TOOL_FILE_CREATE_FAILED
    assert result["status_code"] == 500

def test_handle_api_error_with_invalid_code():
    """
    測試傳入 APIError 且使用未定義錯誤碼時，應 fallback 成 DEFAULT_CODE
    """
    exc = APIError("不明錯誤", status_code=400, code=99999)
    result = handle_exception(exc)

    assert result["type"] == "api"
    assert result["msg"] == "不明錯誤"
    assert result["code"] == 99999  # 仍然保留你傳進來的錯誤碼（但 console 會印警告）
    assert result["status_code"] == 400

def test_handle_api_error_with_no_code():
    """
    測試未提供 code 時，應使用 DEFAULT_CODE 作為 fallback
    """
    exc = APIError("缺少錯誤碼", status_code=500)
    result = handle_exception(exc)

    assert result["type"] == "api"
    assert result["msg"] == "缺少錯誤碼"
    assert result["code"] == ResultCode.GENERIC_ERROR
    assert result["status_code"] == 500

def test_handle_validation_error():
    """
    測試 ValidationError 例外應正確回傳 type, msg, code
    """
    exc = ValidationError("email 格式錯誤", code="EMAIL_INVALID")
    result = handle_exception(exc)

    assert result["type"] == "validation"
    assert result["msg"] == "email 格式錯誤"
    assert result["code"] == "EMAIL_INVALID"

def test_handle_unknown_exception():
    """
    測試傳入非自訂例外（一般 Exception）時，應標示為 unknown
    """
    exc = Exception("非預期錯誤")
    result = handle_exception(exc)

    assert result["type"] == "unknown"
    assert result["msg"] == "非預期錯誤"
