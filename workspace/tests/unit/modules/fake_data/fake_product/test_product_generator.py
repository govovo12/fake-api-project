# workspace/tests/unit/modules/fake_data/fake_product/test_product_generator.py

import pytest
from workspace.modules.fake_data.fake_product.product_generator import generate_product_data
from workspace.config.envs.fake_product_config import CATEGORIES, CATEGORY_IMAGES

pytestmark = [pytest.mark.unit, pytest.mark.fake_product]

def test_product_structure_keys():
    """確認所有必需欄位皆存在"""
    product = generate_product_data()
    expected_keys = {"title", "price", "description", "category", "image"}
    assert expected_keys.issubset(product.keys()), f"Missing keys: {expected_keys - product.keys()}"

def test_category_valid():
    """產生的 category 必定來自 CATEGORIES"""
    product = generate_product_data()
    assert product["category"] in CATEGORIES

def test_image_matches_category():
    """圖片應該對應到分類的 CATEGORY_IMAGES 設定（或 fallback）"""
    product = generate_product_data()
    expected = CATEGORY_IMAGES.get(product["category"])
    if expected:
        assert product["image"] == expected
    else:
        assert product["image"] != ""

def test_price_in_reasonable_range():
    """價格應介於 5 ~ 500（預設產生範圍）"""
    product = generate_product_data()
    assert 5 <= product["price"] <= 500

def test_custom_input_override():
    """自定 title、price、category 應正確覆蓋預設值"""
    custom = {
        "title": "Test Title",
        "price": 999.99,
        "category": "electronics",
        "description": "Custom description",
        "image": "custom.jpg"
    }
    product = generate_product_data(**custom)
    for key in custom:
        assert product[key] == custom[key]
