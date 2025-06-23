# 📦 測試工具
import pytest
from unittest.mock import patch

# 🧪 被測模組
from workspace.controller.data_generation_controller import generate_user_and_product_data

# ⚠️ 錯誤碼常數
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.controller]


@patch("workspace.controller.data_generation_controller.build_cart_data_and_write")
@patch("workspace.controller.data_generation_controller.build_product_data_and_write")
@patch("workspace.controller.data_generation_controller.build_user_data_and_write")
def test_generate_all_success(mock_user, mock_product, mock_cart):
    """
    測試整體測資流程成功：user、product、cart 全部成功
    """
    mock_user.return_value = ResultCode.SUCCESS
    mock_product.return_value = ResultCode.SUCCESS
    mock_cart.return_value = ResultCode.SUCCESS

    result = generate_user_and_product_data("uuid-123")
    assert result == ResultCode.TESTDATA_TASK_SUCCESS
    mock_user.assert_called_once()
    mock_product.assert_called_once()
    mock_cart.assert_called_once()


@patch("workspace.controller.data_generation_controller.build_cart_data_and_write")
@patch("workspace.controller.data_generation_controller.build_product_data_and_write")
@patch("workspace.controller.data_generation_controller.build_user_data_and_write")
def test_generate_user_fail(mock_user, mock_product, mock_cart):
    """
    測試 user 建立失敗，product 與 cart 不應被呼叫
    """
    mock_user.return_value = 40099

    result = generate_user_and_product_data("uuid-123")
    assert result == 40099
    mock_user.assert_called_once()
    mock_product.assert_not_called()
    mock_cart.assert_not_called()


@patch("workspace.controller.data_generation_controller.build_cart_data_and_write")
@patch("workspace.controller.data_generation_controller.build_product_data_and_write")
@patch("workspace.controller.data_generation_controller.build_user_data_and_write")
def test_generate_product_fail(mock_user, mock_product, mock_cart):
    """
    測試 product 建立失敗，cart 不應被呼叫
    """
    mock_user.return_value = ResultCode.SUCCESS
    mock_product.return_value = 40088

    result = generate_user_and_product_data("uuid-123")
    assert result == 40088
    mock_user.assert_called_once()
    mock_product.assert_called_once()
    mock_cart.assert_not_called()


@patch("workspace.controller.data_generation_controller.build_cart_data_and_write")
@patch("workspace.controller.data_generation_controller.build_product_data_and_write")
@patch("workspace.controller.data_generation_controller.build_user_data_and_write")
def test_generate_cart_fail(mock_user, mock_product, mock_cart):
    """
    測試 cart 建立失敗
    """
    mock_user.return_value = ResultCode.SUCCESS
    mock_product.return_value = ResultCode.SUCCESS
    mock_cart.return_value = 41003  # CART_GENERATION_FAILED

    result = generate_user_and_product_data("uuid-123")
    assert result == 41003
    mock_user.assert_called_once()
    mock_product.assert_called_once()
    mock_cart.assert_called_once()
