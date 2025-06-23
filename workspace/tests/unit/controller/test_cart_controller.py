"""
單元測試：購物車子控制器 create_cart_and_report
目標：
- 驗證 retry 行為
- 驗證成功碼轉換與印出
- 驗證錯誤碼是否正確傳遞
"""

# ------------------------
# 📦 測試框架
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
pytestmark = [pytest.mark.unit, pytest.mark.cart, pytest.mark.controller]


class TestCreateCartAndReport:
    @patch("workspace.controller.cart_controller.create_cart")
    @patch("workspace.controller.cart_controller.log_simple_result")
    def test_create_cart_success(self, mock_log, mock_create):
        """✅ 測試購物車建立成功：第一次就成功"""
        mock_create.return_value = (ResultCode.SUCCESS, {"cart": "ok"})

        code, resp = create_cart_and_report("uuid-001", "token-abc")

        assert code == ResultCode.CREATE_CART_SUCCESS
        assert resp == {"cart": "ok"}
        mock_create.assert_called_once()
        mock_log.assert_called_with(ResultCode.CREATE_CART_SUCCESS)

    @patch("workspace.controller.cart_controller.create_cart")
    @patch("workspace.controller.cart_controller.log_simple_result")
    def test_create_cart_retry_then_success(self, mock_log, mock_create):
        """🔁 測試購物車建立成功：前兩次失敗後成功"""
        mock_create.side_effect = [
            (ResultCode.REQUESTS_EXCEPTION, None),
            (ResultCode.SERVER_ERROR, None),
            (ResultCode.SUCCESS, {"cart": "ok"}),
        ]

        code, resp = create_cart_and_report("uuid-002", "token-xyz")

        assert code == ResultCode.CREATE_CART_SUCCESS
        assert resp == {"cart": "ok"}
        assert mock_create.call_count == 3
        mock_log.assert_called_with(ResultCode.CREATE_CART_SUCCESS)

    @patch("workspace.controller.cart_controller.create_cart")
    @patch("workspace.controller.cart_controller.log_simple_result")
    def test_create_cart_all_retries_failed(self, mock_log, mock_create):
        """💥 測試購物車建立失敗：重試三次仍失敗"""
        mock_create.side_effect = [
            (ResultCode.SERVER_ERROR, None),
            (ResultCode.REQUESTS_EXCEPTION, None),
            (ResultCode.SERVER_ERROR, None),
        ]

        code, resp = create_cart_and_report("uuid-003", "token-def")

        assert code == ResultCode.SERVER_ERROR  # ✅ 修正為實際錯誤碼
        assert resp is None
        assert mock_create.call_count == 3
        mock_log.assert_called_with(ResultCode.SERVER_ERROR)

    @patch("workspace.controller.cart_controller.create_cart")
    @patch("workspace.controller.cart_controller.log_simple_result")
    def test_create_cart_non_retryable_error(self, mock_log, mock_create):
        """❌ 測試購物車建立失敗：第一次即遇到非重試錯誤碼"""
        mock_create.return_value = (ResultCode.TOOL_FILE_PERMISSION_DENIED, None)

        code, resp = create_cart_and_report("uuid-004", "token-hij")

        assert code == ResultCode.TOOL_FILE_PERMISSION_DENIED  # ✅ 修正為實際錯誤碼
        assert resp is None
        mock_create.assert_called_once()
        mock_log.assert_called_with(ResultCode.TOOL_FILE_PERMISSION_DENIED)
