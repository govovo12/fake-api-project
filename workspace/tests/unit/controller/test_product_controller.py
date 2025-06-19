import pytest
from unittest.mock import patch, MagicMock
from workspace.controller.product_controller import create_product_and_report
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.product,pytest.mark.controller]


def test_create_product_success():
    """
    正向測試：create_product 回傳成功碼，子控應直接回傳
    """
    with patch("workspace.controller.product_controller.create_product", return_value=(ResultCode.CREATE_PRODUCT_SUCCESS, {"id": 1})):
        code, resp = create_product_and_report("uuid-123", "fake-token")

    assert code == ResultCode.CREATE_PRODUCT_SUCCESS
    assert resp["id"] == 1


def test_create_product_retry_then_success():
    """
    測試遇到可 retry 錯誤碼（6000）後重試成功
    """
    call_sequence = [
        (6000, None),
        (6000, None),
        (ResultCode.CREATE_PRODUCT_SUCCESS, {"id": 2})
    ]

    mock_create = MagicMock(side_effect=call_sequence)

    with patch("workspace.controller.product_controller.create_product", mock_create):
        code, resp = create_product_and_report("uuid-456", "token")

    assert code == ResultCode.CREATE_PRODUCT_SUCCESS
    assert resp["id"] == 2
    assert mock_create.call_count == 3


def test_create_product_server_error_retry_fail():
    """
    測試伺服器錯誤（6001）重試三次仍失敗
    """
    mock_create = MagicMock(return_value=(6001, {"msg": "fail"}))

    with patch("workspace.controller.product_controller.create_product", mock_create):
        code, resp = create_product_and_report("uuid-x", "token")

    assert code == 6001
    assert mock_create.call_count == 3


def test_create_product_non_retryable_error():
    """
    測試遇到非 retry 錯誤碼（如 TOOL_FILE_LOAD_FAILED）時不重試
    """
    mock_create = MagicMock(return_value=(ResultCode.TOOL_FILE_LOAD_FAILED, None))

    with patch("workspace.controller.product_controller.create_product", mock_create):
        code, resp = create_product_and_report("uuid-x", "token")

    assert code == ResultCode.TOOL_FILE_LOAD_FAILED
    assert mock_create.call_count == 1
