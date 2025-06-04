from unittest.mock import MagicMock
from typing import Any, Callable, Optional, Dict

# 📌 Mock 註冊表
_registered_tools: Dict[str, Callable] = {}

def tool(func):
    """即時註冊 mock 工具"""
    _registered_tools[func.__name__] = func
    return func

def get_mock(name: str, *args, **kwargs) -> Any:
    """根據名稱從註冊表中取得 mock"""
    if name not in _registered_tools:
        raise ValueError(f"❌ 無法找到 mock 工具：{name}")
    return _registered_tools[name](*args, **kwargs)

# --- 可用的 mock 工具 ---

@tool
def mock_api_response(status_code: int = 200, json_data: Optional[Any] = None) -> MagicMock:
    """產生模擬 API response 物件"""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data or {}
    return mock_resp

@tool
def mock_function(return_value: Any = None, side_effect: Optional[Callable] = None) -> MagicMock:
    """產生模擬任意函數"""
    return MagicMock(return_value=return_value, side_effect=side_effect)

@tool
def mock_logger() -> MagicMock:
    """產生模擬 logger 物件"""
    logger = MagicMock()
    logger.info = MagicMock()
    logger.warning = MagicMock()
    logger.error = MagicMock()
    logger.debug = MagicMock()
    return logger
