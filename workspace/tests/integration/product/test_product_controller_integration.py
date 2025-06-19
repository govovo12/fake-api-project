import pytest
from unittest.mock import patch, MagicMock
from workspace.controller.product_controller import create_product_and_report
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.integration, pytest.mark.product, pytest.mark.controller]


def test_create_product_integration_success():
    """
    整合測試：任務模組成功回傳，子控應回傳成功碼
    """
    with patch("workspace.modules.product.create_product.get_product_path", return_value="fake.json"), \
         patch("workspace.modules.product.create_product.load_json", return_value={"title": "X"}), \
         patch("workspace.modules.product.create_product.post_and_parse_json", return_value=(200, {"id": 1})):
        code, resp = create_product_and_report("uuid-success", "token")
    assert code == ResultCode.CREATE_PRODUCT_SUCCESS
    assert resp["id"] == 1


def test_create_product_integration_retry_then_success():
    """
    整合測試：第一次與第二次失敗，第三次成功（驗證 retry）
    """
    call_sequence = [
        (503, {"error": "fail"}),           # 第一次：伺服器錯誤
        (500, {"error": "fail again"}),     # 第二次：伺服器錯誤
        (200, {"id": 99})                   # ✅ 第三次：成功
    ]

    with patch("workspace.modules.product.create_product.get_product_path", return_value="fake.json"), \
         patch("workspace.modules.product.create_product.load_json", return_value={"title": "Y"}), \
         patch("workspace.modules.product.create_product.post_and_parse_json", side_effect=call_sequence):
        code, resp = create_product_and_report("uuid-retry", "token")

    assert code == ResultCode.CREATE_PRODUCT_SUCCESS
    assert resp["id"] == 99



def test_create_product_integration_retry_all_fail():
    """
    整合測試：三次皆伺服器錯誤，最終回傳錯誤碼
    """
    fail_response = (503, {"error": "server down"})

    with patch("workspace.modules.product.create_product.get_product_path", return_value="fake.json"), \
         patch("workspace.modules.product.create_product.load_json", return_value={"title": "Z"}), \
         patch("workspace.modules.product.create_product.post_and_parse_json", return_value=fail_response):
        code, resp = create_product_and_report("uuid-fail", "token")

    assert code == ResultCode.SERVER_ERROR
    assert resp["error"] == "server down"
