"""
整合測試：購物車子控制器 create_cart_and_report
目標：
- 驗證 retry 行為是否正確
- 驗證成功是否轉為 CREATE_CART_SUCCESS
- 驗證錯誤是否原樣回傳與印出
"""

# ------------------------
# 📦 測試框架與 mock
# ------------------------
import pytest
from unittest.mock import patch

# ------------------------
# 🧪 被測模組與錯誤碼
# ------------------------
from workspace.controller.cart_controller import create_cart_and_report
from workspace.config.rules.error_codes import ResultCode

# ------------------------
# 🏷️ 測試標記
# ------------------------
pytestmark = [pytest.mark.integration, pytest.mark.cart, pytest.mark.controller]


@patch("workspace.controller.cart_controller.create_cart", return_value=(ResultCode.SUCCESS, {"id": 123}))
@patch("workspace.controller.cart_controller.log_simple_result")
def test_create_cart_success(mock_log, mock_create):
    """✅ 整合：任務模組成功，子控應轉換為 CREATE_CART_SUCCESS"""
    code, resp = create_cart_and_report("uuid-success", "token-abc")
    assert code == ResultCode.CREATE_CART_SUCCESS
    assert resp == {"id": 123}
    mock_create.assert_called_once_with("uuid-success", "token-abc")
    mock_log.assert_called_with(ResultCode.CREATE_CART_SUCCESS)


@patch("workspace.controller.cart_controller.create_cart")
@patch("workspace.controller.cart_controller.log_simple_result")
def test_create_cart_retry_then_success(mock_log, mock_create):
    """🔁 整合：第一次錯誤 → retry 成功"""
    mock_create.side_effect = [
        (ResultCode.SERVER_ERROR, {}),
        (ResultCode.SUCCESS, {"id": 999}),
    ]

    code, resp = create_cart_and_report("uuid-retry", "token-xyz")
    assert code == ResultCode.CREATE_CART_SUCCESS
    assert resp == {"id": 999}
    assert mock_create.call_count == 2
    mock_log.assert_called_with(ResultCode.CREATE_CART_SUCCESS)


@patch("workspace.controller.cart_controller.create_cart")
@patch("workspace.controller.cart_controller.log_simple_result")
def test_create_cart_retry_exhausted(mock_log, mock_create):
    """💥 整合：所有 retry 都失敗，應回傳最後錯誤碼"""
    mock_create.side_effect = [
        (ResultCode.REQUESTS_EXCEPTION, {}),
        (ResultCode.SERVER_ERROR, {}),
        (ResultCode.SERVER_ERROR, {}),
    ]

    code, resp = create_cart_and_report("uuid-fail", "token-xyz")
    assert code == ResultCode.SERVER_ERROR  
    assert resp is None
    assert mock_create.call_count == 3
    mock_log.assert_called_with(ResultCode.SERVER_ERROR) 


@patch("workspace.controller.cart_controller.create_cart", return_value=(ResultCode.TOOL_FILE_PERMISSION_DENIED, {}))
@patch("workspace.controller.cart_controller.log_simple_result")
def test_create_cart_non_retry_error(mock_log, mock_create):
    """❌ 整合：非 retry 錯誤碼（直接返回該錯誤碼）"""
    code, resp = create_cart_and_report("uuid-bad", "token-xyz")
    assert code == ResultCode.TOOL_FILE_PERMISSION_DENIED  
    assert resp is None
    mock_create.assert_called_once()
    mock_log.assert_called_with(ResultCode.TOOL_FILE_PERMISSION_DENIED) 
