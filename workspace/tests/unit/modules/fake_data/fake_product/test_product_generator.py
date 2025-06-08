# workspace/tests/unit/modules/fake_data/fake_product/test_product_generator.py

import pytest
from workspace.modules.fake_data.fake_product.product_generator import generate_product_data
from workspace.config.rules.error_codes import ResultCode

# ✅ pytest 標記（模組分類 + 單元測試）
pytestmark = [pytest.mark.unit, pytest.mark.fake_product]

def test_product_data_keys():
    """
    ✅ 測試：產生的商品資料包含所有必要欄位
    """
    code, product, meta = generate_product_data()
    assert code == ResultCode.SUCCESS, f"錯誤碼: {code}, meta: {meta}"
    expected_keys = {"title", "price", "description", "category", "image"}
    assert expected_keys.issubset(product.keys()), f"缺少欄位: {expected_keys - product.keys()}"

def test_price_range():
    """
    ✅ 測試：價格落在合理範圍（5 ~ 500）
    """
    code, product, meta = generate_product_data()
    assert code == ResultCode.SUCCESS, f"錯誤碼: {code}, meta: {meta}"
    assert 5 <= product["price"] <= 500, f"價格不合理: {product['price']}"

def test_category_is_valid():
    """
    ✅ 測試：商品分類需在 CATEGORIES 列表中
    """
    from workspace.config.envs.fake_product_config import CATEGORIES
    code, product, meta = generate_product_data()
    assert code == ResultCode.SUCCESS, f"錯誤碼: {code}, meta: {meta}"
    assert product["category"] in CATEGORIES, f"分類錯誤: {product['category']} 不在 CATEGORIES 中"

def test_image_url_format():
    """
    ✅ 測試：圖片 URL 格式為 http/https 開頭
    """
    code, product, meta = generate_product_data()
    assert code == ResultCode.SUCCESS, f"錯誤碼: {code}, meta: {meta}"
    assert product["image"].startswith("http"), f"圖片 URL 格式錯誤: {product['image']}"

def test_randomness_of_title():
    """
    ✅ 測試：title 每次產生應不同（簡單比較）
    """
    code1, p1, _ = generate_product_data()
    code2, p2, _ = generate_product_data()
    assert code1 == ResultCode.SUCCESS and code2 == ResultCode.SUCCESS
    assert p1["title"] != p2["title"], "Title 隨機性不足，兩次相同"
