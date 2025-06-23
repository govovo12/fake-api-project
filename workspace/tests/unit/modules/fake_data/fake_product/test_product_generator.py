# 📦 測試工具
import pytest
from unittest.mock import patch

# 🧪 被測模組
from workspace.modules.fake_data.fake_product.product_generator import generate_product_data

# ⚠️ 錯誤碼常數
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.fake_product]


def test_generate_product_data_success():
    """
    測試成功情境：應正確生成所有欄位，category 屬於預設清單
    """
    result = generate_product_data(title="Sample Product", price=199.99)
    assert isinstance(result, dict)
    assert result["title"] == "Sample Product"
    assert result["price"] == 199.99
    assert result["description"].isalnum()
    assert 5 <= len(result["description"]) <= 10
    assert result["image"].startswith("http")
    assert result["category"] in [
        "men's clothing",
        "women's clothing",
        "jewelery",
        "electronics"
    ]


def test_generate_product_data_fallback_title():
    """
    測試 title 為空時，應使用預設值 "Random Product"
    """
    result = generate_product_data(title="", price=50, image="https://example.com/image.png")
    assert result["title"] == "Random Product"


def test_generate_product_data_invalid_price():
    """
    測試 price 為非數字時，應回傳錯誤碼
    """
    result = generate_product_data(title="Sample Product", price="abc")
    assert result == ResultCode.PRODUCT_GENERATION_FAILED


def test_generate_product_data_invalid_image_empty():
    """
    測試當 image 為空字串時，應返回錯誤碼
    """
    result = generate_product_data(title="Sample Product", price=199.99, image="")
    assert result == ResultCode.PRODUCT_GENERATION_FAILED


def test_generate_product_data_invalid_description_length():
    """
    測試 description 長度不符時（如 <5），應回傳錯誤碼
    """
    with patch(
        "workspace.modules.fake_data.fake_product.product_generator.random.choices",
        return_value=list("abc")
    ):
        result = generate_product_data(title="Sample Product", price=199.99)
        assert result == ResultCode.PRODUCT_GENERATION_FAILED
