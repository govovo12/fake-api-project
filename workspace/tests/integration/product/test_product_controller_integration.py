"""
整合測試：商品子控制器 create_product_and_report
目標：
- 驗證成功流程與錯誤流程
- 驗證 retry 行為與最終錯誤碼傳遞
"""

# ------------------------
# 📦 測試框架與 mock
# ------------------------
import pytest
from unittest.mock import patch

# ------------------------
# 🧪 被測模組與錯誤碼
# ------------------------
from workspace.controller.product_controller import create_product_and_report
from workspace.config.rules.error_codes import ResultCode

# ------------------------
# 🏷️ 測試標記
# ------------------------
pytestmark = [pytest.mark.integration, pytest.mark.product, pytest.mark.controller]


def test_create_product_integration_success():
    """✅ 整合：任務模組成功，應轉為 CREATE_PRODUCT_SUCCESS"""
    with patch("workspace.modules.product.create_product.get_product_path", return_value="fake.json"), \
         patch("workspace.modules.product.create_product.load_json", return_value={"title": "A"}), \
         patch("workspace.modules.product.create_product.post_and_parse_json", return_value=(200, {"id": 1})):
        code, resp = create_product_and_report("uuid-ok", "token")

    assert code == ResultCode.CREATE_PRODUCT_SUCCESS
    assert resp["id"] == 1


def test_create_product_integration_retry_then_success():
    """🔁 整合：重試兩次後成功（應轉為 CREATE_PRODUCT_SUCCESS）"""

    with patch("workspace.controller.product_controller.create_product", side_effect=[
        (ResultCode.SERVER_ERROR, None),
        (ResultCode.REQUESTS_EXCEPTION, None),
        (ResultCode.SUCCESS, {"id": 2}),
    ]):
        code, resp = create_product_and_report("uuid-retry", "token")

    assert code == ResultCode.CREATE_PRODUCT_SUCCESS
    assert resp["id"] == 2




def test_create_product_integration_retry_all_fail():
    """💥 整合：重試三次失敗，最終應回傳 SERVER_ERROR"""
    with patch("workspace.modules.product.create_product.get_product_path", return_value="fake.json"), \
         patch("workspace.modules.product.create_product.load_json", return_value={"title": "C"}), \
         patch("workspace.modules.product.create_product.post_and_parse_json", return_value=(503, {"error": "server down"})):
        code, resp = create_product_and_report("uuid-fail", "token")

    assert code == ResultCode.SERVER_ERROR
    assert resp is None  
