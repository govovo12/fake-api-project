import pytest
from unittest.mock import patch
from workspace.controller.data_generation_controller import generate_user_and_product_data
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.controller]

@patch("workspace.controller.data_generation_controller.print_trace")
@patch("workspace.controller.data_generation_controller.log_simple_result")
@patch("workspace.controller.data_generation_controller.build_product_data_and_write")
@patch("workspace.controller.data_generation_controller.build_user_data_and_write")
def test_generate_all_success(mock_user, mock_product, mock_log, mock_trace):
    mock_user.return_value = ResultCode.SUCCESS
    mock_product.return_value = ResultCode.SUCCESS

    result = generate_user_and_product_data("abc123")

    mock_trace.assert_called_once()
    assert mock_log.call_count == 3
    assert result == ResultCode.TESTDATA_TASK_SUCCESS

@patch("workspace.controller.data_generation_controller.print_trace")
@patch("workspace.controller.data_generation_controller.log_simple_result")
@patch("workspace.controller.data_generation_controller.build_product_data_and_write")
@patch("workspace.controller.data_generation_controller.build_user_data_and_write")
def test_generate_user_fail(mock_user, mock_product, mock_log, mock_trace):
    mock_user.return_value = ResultCode.FAKER_GENERATE_FAILED

    result = generate_user_and_product_data("abc123")

    mock_trace.assert_called_once()
    mock_log.assert_called_once_with(ResultCode.FAKER_GENERATE_FAILED)
    mock_product.assert_not_called()
    assert result == ResultCode.FAKER_GENERATE_FAILED

@patch("workspace.controller.data_generation_controller.print_trace")
@patch("workspace.controller.data_generation_controller.log_simple_result")
@patch("workspace.controller.data_generation_controller.build_product_data_and_write")
@patch("workspace.controller.data_generation_controller.build_user_data_and_write")
def test_generate_product_fail(mock_user, mock_product, mock_log, mock_trace):
    mock_user.return_value = ResultCode.SUCCESS
    mock_product.return_value = ResultCode.PRODUCT_GENERATION_FAILED

    result = generate_user_and_product_data("abc123")

    assert mock_log.call_count == 2  # user success, product fail
    assert result == ResultCode.PRODUCT_GENERATION_FAILED
