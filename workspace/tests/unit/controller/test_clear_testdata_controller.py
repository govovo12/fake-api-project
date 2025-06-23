"""
單元測試：clear_user_and_product_data 子控制器
測試目標：
- 驗證刪除流程是否中止於錯誤發生點
- 驗證正確轉換成功碼與印出錯誤碼
"""

# ------------------------
# 📦 測試框架與 Patch
# ------------------------
import pytest
from unittest.mock import patch

# ------------------------
# 🧪 被測模組與錯誤碼
# ------------------------
from workspace.controller.clear_testdata_controller import clear_user_and_product_data
from workspace.config.rules.error_codes import ResultCode

# ------------------------
# 🏷️ 測試標記
# ------------------------
pytestmark = [pytest.mark.unit, pytest.mark.cleaner, pytest.mark.controller]



class TestClearTestdataController:
    """單元測試：clear_user_and_product_data 子控制器"""

    @patch("workspace.utils.retry.retry_handler.retry_on_code", side_effect=lambda f, **kwargs: (lambda u: f(u)))
    @patch("workspace.controller.clear_testdata_controller.remove_user_data", return_value=ResultCode.SUCCESS)
    @patch("workspace.controller.clear_testdata_controller.remove_product_data", return_value=ResultCode.SUCCESS)
    @patch("workspace.controller.clear_testdata_controller.remove_cart_data", return_value=ResultCode.SUCCESS)
    @patch("workspace.controller.clear_testdata_controller.log_simple_result")
    def test_clear_all_success(self, mock_log, mock_cart, mock_product, mock_user, mock_retry):
        """三個任務模組皆成功，回傳測資清除成功碼"""
        code = clear_user_and_product_data("uuid-001")
        assert code == ResultCode.TASK_CLEAN_TESTDATA_SUCCESS
        mock_user.assert_called_once()
        mock_product.assert_called_once()
        mock_cart.assert_called_once()
        mock_log.assert_called_with(ResultCode.TASK_CLEAN_TESTDATA_SUCCESS)

    @patch("workspace.utils.retry.retry_handler.retry_on_code", side_effect=lambda f, **kwargs: (lambda u: f(u)))
    @patch("workspace.controller.clear_testdata_controller.remove_user_data", return_value=ResultCode.REMOVE_USER_DATA_FAILED)
    @patch("workspace.controller.clear_testdata_controller.remove_product_data")
    @patch("workspace.controller.clear_testdata_controller.remove_cart_data")
    @patch("workspace.controller.clear_testdata_controller.log_simple_result")
    def test_clear_user_failed(self, mock_log, mock_cart, mock_product, mock_user, mock_retry):
        """若刪除 user 測資失敗，應立即中止並回傳錯誤碼"""
        code = clear_user_and_product_data("uuid-err1")
        assert code == ResultCode.REMOVE_USER_DATA_FAILED
        mock_user.assert_called_once()
        mock_product.assert_not_called()
        mock_cart.assert_not_called()
        mock_log.assert_called_with(ResultCode.REMOVE_USER_DATA_FAILED)

    @patch("workspace.utils.retry.retry_handler.retry_on_code", side_effect=lambda f, **kwargs: (lambda u: f(u)))
    @patch("workspace.controller.clear_testdata_controller.remove_user_data", return_value=ResultCode.SUCCESS)
    @patch("workspace.controller.clear_testdata_controller.remove_product_data", return_value=ResultCode.REMOVE_PRODUCT_DATA_FAILED)
    @patch("workspace.controller.clear_testdata_controller.remove_cart_data")
    @patch("workspace.controller.clear_testdata_controller.log_simple_result")
    def test_clear_product_failed(self, mock_log, mock_cart, mock_product, mock_user, mock_retry):
        """user 成功、product 失敗，應中止流程"""
        code = clear_user_and_product_data("uuid-err2")
        assert code == ResultCode.REMOVE_PRODUCT_DATA_FAILED
        mock_user.assert_called_once()
        mock_product.assert_called_once()
        mock_cart.assert_not_called()
        mock_log.assert_called_with(ResultCode.REMOVE_PRODUCT_DATA_FAILED)

    @patch("workspace.utils.retry.retry_handler.retry_on_code", side_effect=lambda f, **kwargs: (lambda u: f(u)))
    @patch("workspace.controller.clear_testdata_controller.remove_user_data", return_value=ResultCode.SUCCESS)
    @patch("workspace.controller.clear_testdata_controller.remove_product_data", return_value=ResultCode.SUCCESS)
    @patch("workspace.controller.clear_testdata_controller.remove_cart_data", return_value=ResultCode.REMOVE_CART_DATA_FAILED)
    @patch("workspace.controller.clear_testdata_controller.log_simple_result")
    def test_clear_cart_failed(self, mock_log, mock_cart, mock_product, mock_user, mock_retry):
        """user 與 product 成功，但 cart 刪除失敗"""
        code = clear_user_and_product_data("uuid-err3")
        assert code == ResultCode.REMOVE_CART_DATA_FAILED
        mock_user.assert_called_once()
        mock_product.assert_called_once()
        mock_cart.assert_called_once()
        mock_log.assert_called_with(ResultCode.REMOVE_CART_DATA_FAILED)
