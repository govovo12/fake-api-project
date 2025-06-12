import pytest
from unittest.mock import patch
from workspace.config.rules.error_codes import ResultCode
from modules.fake_data.fake_product.product_generator import generate_product_data

# 測試標記
pytestmark = [pytest.mark.unit, pytest.mark.fake_product]

def test_generate_product_data_success():
    """
    測試成功情境：
    應正確生成所有欄位，category 一定屬於 CATEGORY_LIST
    """
    result = generate_product_data(title="Sample Product", price=199.99)

    # 檢查商品資料生成
    assert isinstance(result, dict)
    assert result["title"] == "Sample Product"
    assert result["price"] == 199.99
    assert result["description"].isalnum()  # 檢查 description 是否符合格式
    assert 5 <= len(result["description"]) <= 10  # 檢查 description 長度
    assert result["image"].startswith("http")  # 檢查 image 是否以 http 開頭
    assert result["category"] in ["Clothes", "Electronics", "Jewelery", "Men's Clothing", "Women's Clothing"]

def test_generate_product_data_invalid_title():
    """
    測試 title 為空時，應該使用預設值 "Random Product"
    """
    result = generate_product_data(title="", price=50)
    assert result["title"] == "Random Product"

def test_generate_product_data_invalid_price():
    """
    測試 price 為非數字時，應該返回錯誤碼
    """
    result = generate_product_data(title="Sample Product", price="abc")
    assert result == ResultCode.PRODUCT_GENERATION_FAILED

def test_generate_product_data_category_empty():
    """
    測試當隨機選擇的 category 為不在 CATEGORY_LIST 的值時，應該返回 PRODUCT_CATEGORY_EMPTY
    """
    with patch('random.choice', return_value="AAA"):  # 模擬隨機選擇非法值 "AAA"
        result = generate_product_data(title="Sample Product", price=99.99, category=None)
        
        # 檢查錯誤碼，應該返回 PRODUCT_CATEGORY_EMPTY
        assert result == ResultCode.PRODUCT_CATEGORY_EMPTY

def test_generate_product_data_invalid_image_empty():
    """
    測試當 image 為空時，應返回錯誤碼 PRODUCT_GENERATION_FAILED
    """
    # 模擬 image 為空
    result = generate_product_data(title="Sample Product", price=199.99, category="electronics")
    
    # 強制將 image 設為空
    result["image"] = ""  # 強制將 image 設為空
    
    # 檢查是否返回錯誤碼
    assert result == ResultCode.PRODUCT_GENERATION_FAILED


def test_generate_product_data_invalid_description():
    """
    測試當 description 格式不正確（長度不符）時，應返回錯誤碼
    """
    # 模擬生成的 description 長度不符
    result = generate_product_data(title="Sample Product", price=199.99)
    
    # 如果 description 長度小於 5 或大於 10，應該返回錯誤碼
    assert result == ResultCode.PRODUCT_GENERATION_FAILED
