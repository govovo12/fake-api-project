from unittest.mock import MagicMock
from typing import Any, Callable, Optional

def tool(func):
    func.is_tool = True
    return func

@tool
def mock_api_response(status_code: int = 200, json_data: Optional[Any] = None) -> MagicMock:
    """產生模擬 API response 物件 [TOOL]"""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data or {}
    return mock_resp

@tool
def mock_function(return_value: Any = None, side_effect: Optional[Callable] = None) -> MagicMock:
    """產生模擬任意函數的 MagicMock [TOOL]"""
    return MagicMock(return_value=return_value, side_effect=side_effect)

@tool
def mock_logger() -> MagicMock:
    """產生模擬 logger 物件 [TOOL]"""
    logger = MagicMock()
    logger.info = MagicMock()
    logger.warning = MagicMock()
    logger.error = MagicMock()
    logger.debug = MagicMock()
    return logger
