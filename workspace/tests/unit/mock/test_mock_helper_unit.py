import pytest
from utils.mock.mock_helper import mock_api_response, mock_function, mock_logger

pytestmark = [pytest.mark.unit, pytest.mark.mock]

def test_mock_api_response_returns_correct_status():
    """驗證 status_code 與 json 回傳正確"""
    mock_resp = mock_api_response(status_code=201, json_data={"msg": "created"})
    assert mock_resp.status_code == 201
    assert mock_resp.json() == {"msg": "created"}

def test_mock_function_with_return_value():
    """驗證 mock function 回傳值"""
    mock_func = mock_function(return_value=42)
    assert mock_func() == 42

def test_mock_function_with_side_effect():
    """驗證 mock function 可拋異常"""
    mock_func = mock_function(side_effect=ValueError("test error"))
    with pytest.raises(ValueError) as exc_info:
        mock_func()
    assert "test error" in str(exc_info.value)

def test_mock_logger_methods_are_callable():
    """驗證 mock_logger 所有 log 方法可呼叫、可 assert"""
    logger = mock_logger()
    logger.info("info message")
    logger.warning("warn message")
    logger.error("error message")
    logger.debug("debug message")
    logger.info.assert_called_with("info message")
    logger.warning.assert_called_with("warn message")
    logger.error.assert_called_with("error message")
    logger.debug.assert_called_with("debug message")
