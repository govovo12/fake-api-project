import pytest
from workspace.controller.data_generation_controller import generate_user_and_product_data
from workspace.config.rules.error_codes import ResultCode
from unittest.mock import patch

pytestmark = [pytest.mark.integration, pytest.mark.controller]

@patch("workspace.controller.data_generation_controller.log_simple_result")
def test_integrated_all_success(mock_log):
    """
    整合測試：三組合器都成功 → 回傳 TESTDATA_TASK_SUCCESS，log 應呼叫 4 次
    """
    uuid = "1234567890abcdef1234567890abcdef"
    result = generate_user_and_product_data(uuid)

    assert result == ResultCode.TESTDATA_TASK_SUCCESS
    assert mock_log.call_count == 4
    mock_log.assert_called_with(ResultCode.TESTDATA_TASK_SUCCESS)


@patch("workspace.controller.data_generation_controller.log_simple_result")
def test_integrated_user_fail(mock_log, monkeypatch):
    """
    整合測試：user 組合器失敗 → 中斷流程，不執行 product，log 應呼叫 1 次
    """
    def fake_user_fail(uuid):
        return ResultCode.FAKER_GENERATE_FAILED

    monkeypatch.setattr(
        "workspace.controller.data_generation_controller.build_user_data_and_write",
        fake_user_fail
    )

    result = generate_user_and_product_data("abc123")
    assert result == ResultCode.FAKER_GENERATE_FAILED
    mock_log.assert_called_once_with(ResultCode.FAKER_GENERATE_FAILED)


@patch("workspace.controller.data_generation_controller.log_simple_result")
def test_integrated_product_fail(mock_log, monkeypatch):
    """
    整合測試：user 成功但 product 失敗 → 回傳 product 錯誤碼，log 應呼叫 2 次
    """
    monkeypatch.setattr(
        "workspace.controller.data_generation_controller.build_user_data_and_write",
        lambda uuid: ResultCode.SUCCESS
    )

    def fake_product_fail(uuid):
        return ResultCode.PRODUCT_GENERATION_FAILED

    monkeypatch.setattr(
        "workspace.controller.data_generation_controller.build_product_data_and_write",
        fake_product_fail
    )

    result = generate_user_and_product_data("abc123")
    assert result == ResultCode.PRODUCT_GENERATION_FAILED
    assert mock_log.call_count == 2
    mock_log.assert_called_with(ResultCode.PRODUCT_GENERATION_FAILED)
    
@patch("workspace.controller.data_generation_controller.log_simple_result")
def test_integrated_cart_fail(mock_log, monkeypatch):
    """
    整合測試：cart 組合器失敗 → 中斷流程，log 應呼叫 3 次
    """
    monkeypatch.setattr(
        "workspace.controller.data_generation_controller.build_user_data_and_write",
        lambda uuid: ResultCode.SUCCESS
    )
    monkeypatch.setattr(
        "workspace.controller.data_generation_controller.build_product_data_and_write",
        lambda uuid: ResultCode.SUCCESS
    )
    monkeypatch.setattr(
        "workspace.controller.data_generation_controller.build_cart_data_and_write",
        lambda uuid: 41003  # CART_GENERATION_FAILED
    )

    result = generate_user_and_product_data("uuid-xyz")
    assert result == 41003
    assert mock_log.call_count == 3
    mock_log.assert_called_with(41003)
