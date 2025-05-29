from unittest.mock import MagicMock

def mock_api_response(status_code=200, json_data=None):
    """
    回傳模擬 API response 物件。
    :param status_code: 回傳的狀態碼，預設為 200
    :param json_data: 回傳的 JSON 內容，預設為空 dict
    :return: MagicMock 物件，模擬 response
    """
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = json_data or {}
    return mock_resp

def mock_function(return_value=None, side_effect=None):
    """
    回傳模擬任意函數的 MagicMock。
    :param return_value: 預設回傳值
    :param side_effect: 模擬副作用（可丟入 Exception 或函數）
    :return: MagicMock 物件
    """
    return MagicMock(return_value=return_value, side_effect=side_effect)

def mock_logger():
    """
    模擬 logger 物件，具備 info, warn, error 等方法。
    用於取代真實 logger，以免測試寫入實體 log。
    :return: MagicMock 物件，具備常見 log 方法
    """
    logger = MagicMock()
    logger.info = MagicMock()
    logger.warning = MagicMock()
    logger.error = MagicMock()
    logger.debug = MagicMock()
    return logger
