"""
單元測試：商品子控制器 create_product_and_report
目標：
- 驗證 retry 行為與錯誤碼傳遞
- 成功時轉為 CREATE_PRODUCT_SUCCESS 並印出
"""

# ------------------------
# 📦 測試框架與 mock
# ------------------------
import pytest
from unittest.mock import patch, MagicMock

# ------------------------
# 🧪 被測模組與錯誤碼
# ------------------------
from workspace.controller.product_controller import create_product_and_report
from workspace.config.rules.error_codes import ResultCode

# ------------------------
# 🏷️ 測試標記
# ------------------------
pytestmark = [pytest.mark.unit, pytest.mark.product, pytest.mark.controller]


def test_create_product_success():
    """✅ 測試任務模組成功，子控應轉換為 CREATE_PRODUCT_SUCCESS"""
    with patch("workspace.controller.product_controller.create_product", return_value=(ResultCode.SUCCESS, {"id": 1})):
        code, resp = create_product_and_report("uuid-123", "fake-token")

    assert code == ResultCode.CREATE_PRODUCT_SUCCESS
    assert resp["id"] == 1


def test_create_product_retry_then_success():
    """🔁 測試遇到可 retry 錯誤後重試成功"""
    call_sequence = [
        (ResultCode.REQUESTS_EXCEPTION, None),
        (ResultCode.SERVER_ERROR, None),
        (ResultCode.SUCCESS, {"id": 2})
    ]

    mock_create = MagicMock(side_effect=call_sequence)

    with patch("workspace.controller.product_controller.create_product", mock_create):
        code, resp = create_product_and_report("uuid-456", "token")

    assert code == ResultCode.CREATE_PRODUCT_SUCCESS
    assert resp["id"] == 2
    assert mock_create.call_count == 3


def test_create_product_server_error_retry_fail():
    """💥 測試伺服器錯誤重試三次仍失敗"""
    mock_create = MagicMock(return_value=(ResultCode.SERVER_ERROR, {"msg": "fail"}))

    with patch("workspace.controller.product_controller.create_product", mock_create):
        code, resp = create_product_and_report("uuid-x", "token")

    assert code == ResultCode.SERVER_ERROR
    assert resp is None
    assert mock_create.call_count == 3


def test_create_product_non_retryable_error():
    """❌ 測試遇到非 retry 錯誤碼（如 TOOL_FILE_LOAD_FAILED）時不重試"""
    mock_create = MagicMock(return_value=(ResultCode.TOOL_FILE_LOAD_FAILED, None))

    with patch("workspace.controller.product_controller.create_product", mock_create):
        code, resp = create_product_and_report("uuid-x", "token")

    assert code == ResultCode.TOOL_FILE_LOAD_FAILED
    assert resp is None
    assert mock_create.call_count == 1
