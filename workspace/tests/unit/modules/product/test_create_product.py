"""
單元測試：create_product 任務模組
測試目標：
- 成功建立商品
- 檔案格式錯誤、例外處理、API 回傳異常等錯誤碼處理
"""

# ------------------------
# 📦 測試框架與工具
# ------------------------
import pytest
import json
from pathlib import Path
from unittest.mock import patch

# ------------------------
# 🧪 被測模組與錯誤碼
# ------------------------
from workspace.modules.product.create_product import create_product
from workspace.config.rules.error_codes import ResultCode

# ------------------------
# 🏷️ 測試標記
# ------------------------
pytestmark = [pytest.mark.unit, pytest.mark.product]


def test_create_product_success(tmp_path):
    """✅ 正向測試：成功讀取測資並建立商品（HTTP 200）"""
    uuid = "test123"
    fake_payload_path = tmp_path / f"{uuid}.json"
    fake_payload = {
        "title": "Product A",
        "price": 100,
        "description": "desc",
        "image": "https://fakeimg.pl/250x250/",
        "category": "electronics"
    }

    with open(fake_payload_path, "w", encoding="utf-8") as f:
        json.dump(fake_payload, f)

    with patch("workspace.modules.product.create_product.get_product_path", return_value=fake_payload_path), \
         patch("workspace.modules.product.create_product.post_and_parse_json", return_value=(200, {"id": 1})):
        code, resp = create_product(uuid)

    assert code == ResultCode.SUCCESS  
    assert isinstance(resp, dict)
    assert resp["id"] == 1


def test_create_product_invalid_payload():
    """❌ 邊界測試：JSON 資料非 dict 結構"""
    with patch("workspace.modules.product.create_product.get_product_path", return_value=Path("fake.json")), \
         patch("workspace.modules.product.create_product.load_json", return_value=["not", "a", "dict"]):
        code, resp = create_product("test456")

    assert code == ResultCode.TOOL_FILE_LOAD_FAILED
    assert resp is None


def test_create_product_server_error():
    """💥 錯誤測試：伺服器回傳 HTTP 5xx"""
    with patch("workspace.modules.product.create_product.get_product_path", return_value=Path("test.json")), \
         patch("workspace.modules.product.create_product.load_json", return_value={"title": "A"}), \
         patch("workspace.modules.product.create_product.post_and_parse_json", return_value=(503, {"error": "server down"})):
        code, resp = create_product("test789")

    assert code == ResultCode.SERVER_ERROR  
    assert resp.get("error") == "server down"


def test_create_product_request_exception():
    """💥 例外測試：發生 requests 例外（如連線失敗）"""
    with patch("workspace.modules.product.create_product.get_product_path", return_value=Path("test.json")), \
         patch("workspace.modules.product.create_product.load_json", return_value={"title": "A"}), \
         patch("workspace.modules.product.create_product.post_and_parse_json", side_effect=Exception("network error")):
        code, resp = create_product("test999")

    assert code == ResultCode.REQUESTS_EXCEPTION  
    assert resp is None
