import pytest
from utils.mock.mock_helper import get_mock

pytestmark = [pytest.mark.unit, pytest.mark.mock]

def test_get_mock_api_response():
    mock_resp = get_mock("mock_api_response", status_code=201, json_data={"msg": "created"})
    assert mock_resp.status_code == 201
    assert mock_resp.json() == {"msg": "created"}

def test_get_mock_function_with_return_value():
    mock_func = get_mock("mock_function", return_value=42)
    assert mock_func() == 42

def test_get_mock_function_with_side_effect():
    mock_func = get_mock("mock_function", side_effect=ValueError("test error"))
    with pytest.raises(ValueError) as exc_info:
        mock_func()
    assert "test error" in str(exc_info.value)

def test_get_mock_logger_methods_callable():
    logger = get_mock("mock_logger")
    logger.info("info message")
    logger.warning("warn message")
    logger.error("error message")
    logger.debug("debug message")
    logger.info.assert_called_with("info message")
    logger.warning.assert_called_with("warn message")
    logger.error.assert_called_with("error message")
    logger.debug.assert_called_with("debug message")
