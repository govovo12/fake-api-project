import pytest
from workspace.modules.fake_data.fake_product.product_generator import generate_product_data
from workspace.config.envs.fake_product_config import CATEGORIES

pytestmark = [pytest.mark.unit, pytest.mark.fake_product]


def test_product_data_keys():
    success, product, meta = generate_product_data()
    assert success is True, f"產生失敗: {meta}"
    expected_keys = {"title", "price", "description", "category", "image"}
    assert expected_keys.issubset(product.keys()), f"缺少欄位: {expected_keys - product.keys()}"


def test_price_range():
    success, product, meta = generate_product_data()
    assert success is True
    assert 5 <= product["price"] <= 500, f"價格不合理: {product['price']}"


def test_category_is_valid():
    success, product, meta = generate_product_data()
    assert success is True
    assert product["category"] in CATEGORIES, f"分類錯誤: {product['category']} 不在 CATEGORIES 中"


def test_image_url_format():
    success, product, meta = generate_product_data()
    assert success is True
    assert product["image"].startswith("http"), f"圖片 URL 格式錯誤: {product['image']}"


def test_randomness_of_title():
    success1, p1, _ = generate_product_data()
    success2, p2, _ = generate_product_data()
    assert success1 and success2
    assert p1["title"] != p2["title"], "Title 隨機性不足，兩次相同"
