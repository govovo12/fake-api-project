import pytest
from workspace.modules.fake_data.fake_product.product_generator import generate_product_data
from workspace.config.envs.fake_product_config import CATEGORIES, CATEGORY_IMAGES
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.fake_product]

def test_product_structure_keys():
    """確認所有必需欄位皆存在"""
    code, product = generate_product_data()
    assert code == ResultCode.SUCCESS
    expected_keys = {"title", "price", "description", "category", "image"}
    assert expected_keys.issubset(product.keys()), f"Missing keys: {expected_keys - product.keys()}"

def test_category_valid():
    """產生的 category 必定來自 CATEGORIES"""
    code, product = generate_product_data()
    assert code == ResultCode.SUCCESS
    assert product["category"] in CATEGORIES

def test_image_matches_category():
    """圖片應該對應到分類的 CATEGORY_IMAGES 設定（或 fallback）"""
    code, product = generate_product_data()
    assert code == ResultCode.SUCCESS
    expected = CATEGORY_IMAGES.get(product["category"])
    if expected:
        assert product["image"] == expected
    else:
        assert product["image"] != ""

def test_price_in_reasonable_range():
    """價格應介於 5 ~ 500（預設產生範圍）"""
    code, product = generate_product_data()
    assert code == ResultCode.SUCCESS
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
    code, product = generate_product_data(**custom)
    assert code == ResultCode.SUCCESS
    for key in custom:
        assert product[key] == custom[key]
def test_fail_when_no_categories(monkeypatch):
    """當 CATEGORIES 為空，應回傳錯誤碼並且不產生資料"""
    monkeypatch.setattr("workspace.modules.fake_data.fake_product.product_generator.CATEGORIES", [])
    code, product = generate_product_data()
    assert code == ResultCode.PRODUCT_GEN_FAIL
    assert product is None
