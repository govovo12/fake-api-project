"""
整合測試：clear_user_and_product_data 子控制器
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
pytestmark = [pytest.mark.integration, pytest.mark.cleaner, pytest.mark.controller]


def test_clear_testdata_success():
    """✅ 整合：三個模組皆成功應回傳 TASK_CLEAN_TESTDATA_SUCCESS"""
    with patch("workspace.controller.clear_testdata_controller.remove_user_data", return_value=ResultCode.SUCCESS), \
         patch("workspace.controller.clear_testdata_controller.remove_product_data", return_value=ResultCode.SUCCESS), \
         patch("workspace.controller.clear_testdata_controller.remove_cart_data", return_value=ResultCode.SUCCESS), \
         patch("workspace.controller.clear_testdata_controller.log_simple_result") as mock_log:

        code = clear_user_and_product_data("uuid-001")

    assert code == ResultCode.TASK_CLEAN_TESTDATA_SUCCESS
    mock_log.assert_called_with(ResultCode.TASK_CLEAN_TESTDATA_SUCCESS)


def test_clear_testdata_fail_on_user():
    """❌ 整合：user 刪除失敗，流程應中止"""
    with patch("workspace.controller.clear_testdata_controller.remove_user_data", return_value=ResultCode.REMOVE_USER_DATA_FAILED), \
         patch("workspace.controller.clear_testdata_controller.remove_product_data") as mock_p, \
         patch("workspace.controller.clear_testdata_controller.remove_cart_data") as mock_c, \
         patch("workspace.controller.clear_testdata_controller.log_simple_result") as mock_log:

        code = clear_user_and_product_data("uuid-userfail")

    assert code == ResultCode.REMOVE_USER_DATA_FAILED
    mock_p.assert_not_called()
    mock_c.assert_not_called()
    mock_log.assert_called_with(ResultCode.REMOVE_USER_DATA_FAILED)


def test_clear_testdata_fail_on_product():
    """❌ 整合：product 刪除失敗，流程應中止於第二步"""
    with patch("workspace.controller.clear_testdata_controller.remove_user_data", return_value=ResultCode.SUCCESS), \
         patch("workspace.controller.clear_testdata_controller.remove_product_data", return_value=ResultCode.REMOVE_PRODUCT_DATA_FAILED), \
         patch("workspace.controller.clear_testdata_controller.remove_cart_data") as mock_c, \
         patch("workspace.controller.clear_testdata_controller.log_simple_result") as mock_log:

        code = clear_user_and_product_data("uuid-prod-fail")

    assert code == ResultCode.REMOVE_PRODUCT_DATA_FAILED
    mock_c.assert_not_called()
    mock_log.assert_called_with(ResultCode.REMOVE_PRODUCT_DATA_FAILED)


def test_clear_testdata_fail_on_cart():
    """❌ 整合：cart 刪除失敗，流程應中止於第三步"""
    with patch("workspace.controller.clear_testdata_controller.remove_user_data", return_value=ResultCode.SUCCESS), \
         patch("workspace.controller.clear_testdata_controller.remove_product_data", return_value=ResultCode.SUCCESS), \
         patch("workspace.controller.clear_testdata_controller.remove_cart_data", return_value=ResultCode.REMOVE_CART_DATA_FAILED), \
         patch("workspace.controller.clear_testdata_controller.log_simple_result") as mock_log:

        code = clear_user_and_product_data("uuid-cart-fail")

    assert code == ResultCode.REMOVE_CART_DATA_FAILED
    mock_log.assert_called_with(ResultCode.REMOVE_CART_DATA_FAILED)
