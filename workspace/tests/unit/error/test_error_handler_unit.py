import pytest
from workspace.utils.error.error_handler import APIError, ValidationError, handle_exception
from workspace.config.rules import error_codes

pytestmark = pytest.mark.error

def test_handle_api_error():
    err = APIError("API failed", status_code=500, code=error_codes.API_RESPONSE_FORMAT_ERROR)
    result = handle_exception(err)
    assert result["type"] == "api"
    assert result["code"] == error_codes.API_RESPONSE_FORMAT_ERROR
    assert result["status_code"] == 500
    assert result["msg"] == "API failed"

def test_handle_validation_error():
    err = ValidationError("Missing required fields")
    result = handle_exception(err)
    assert result["type"] == "validation"
    assert result["code"] == "VALIDATION_ERROR"
    assert result["msg"] == "Missing required fields"

def test_handle_unknown_error():
    err = RuntimeError("Something went wrong")
    result = handle_exception(err)
    assert result["type"] == "unknown"
    assert result["msg"] == "Something went wrong"