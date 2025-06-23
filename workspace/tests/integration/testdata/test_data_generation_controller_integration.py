# 📦 測試工具
import pytest
from unittest.mock import patch

# 🧪 被測模組
from workspace.controller.data_generation_controller import generate_user_and_product_data

# ⚠️ 錯誤碼常數
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.integration, pytest.mark.controller]


@patch("workspace.controller.data_generation_controller.build_user_data_and_write", return_value=ResultCode.SUCCESS)
@patch("workspace.controller.data_generation_controller.build_product_data_and_write", return_value=ResultCode.SUCCESS)
@patch("workspace.controller.data_generation_controller.build_cart_data_and_write", return_value=ResultCode.SUCCESS)
def test_all_success(mock_cart, mock_product, mock_user):
    """
    整合測試：所有模組成功，應回傳 TESTDATA_TASK_SUCCESS
    """
    result = generate_user_and_product_data("uuid-001")
    assert result == ResultCode.TESTDATA_TASK_SUCCESS


@patch("workspace.controller.data_generation_controller.build_user_data_and_write", return_value=ResultCode.FAKER_GENERATE_FAILED)
@patch("workspace.controller.data_generation_controller.build_product_data_and_write", return_value=ResultCode.SUCCESS)
@patch("workspace.controller.data_generation_controller.build_cart_data_and_write", return_value=ResultCode.SUCCESS)
def test_build_user_failed(mock_cart, mock_product, mock_user):
    """
    整合測試：user 測資失敗，應中斷並回傳 FAKER_GENERATE_FAILED
    """
    result = generate_user_and_product_data("uuid-002")
    assert result == ResultCode.FAKER_GENERATE_FAILED


@patch("workspace.controller.data_generation_controller.build_user_data_and_write", return_value=ResultCode.SUCCESS)
@patch("workspace.controller.data_generation_controller.build_product_data_and_write", return_value=ResultCode.PRODUCT_GENERATION_FAILED)
@patch("workspace.controller.data_generation_controller.build_cart_data_and_write", return_value=ResultCode.SUCCESS)
def test_build_product_failed(mock_cart, mock_product, mock_user):
    """
    整合測試：product 測資失敗，應中斷並回傳 PRODUCT_GENERATION_FAILED
    """
    result = generate_user_and_product_data("uuid-003")
    assert result == ResultCode.PRODUCT_GENERATION_FAILED


@patch("workspace.controller.data_generation_controller.build_user_data_and_write", return_value=ResultCode.SUCCESS)
@patch("workspace.controller.data_generation_controller.build_product_data_and_write", return_value=ResultCode.SUCCESS)
@patch("workspace.controller.data_generation_controller.build_cart_data_and_write", return_value=ResultCode.CART_GENERATION_FAILED)
def test_build_cart_failed(mock_cart, mock_product, mock_user):
    """
    整合測試：cart 測資失敗，應中斷並回傳 CART_GENERATION_FAILED
    """
    result = generate_user_and_product_data("uuid-004")
    assert result == ResultCode.CART_GENERATION_FAILED
