# workspace/tests/unit/fake/test_fake_helper_unit.py

import re
import pytest
from workspace.utils.fake.fake_helper import *

pytestmark = [pytest.mark.fake, pytest.mark.unit]

# ==== 帳號相關 ====

def test_fake_username_type_and_not_empty():
    """fake_username 回傳型態與非空檢查"""
    val = fake_username()
    assert isinstance(val, str)
    assert val

def test_fake_password_type_and_not_empty():
    """fake_password 回傳型態與非空檢查"""
    val = fake_password()
    assert isinstance(val, str)
    assert val

def test_fake_email_format():
    """fake_email 型態與格式檢查"""
    val = fake_email()
    assert isinstance(val, str)
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    assert re.match(pattern, val)

def test_fake_phone_type_and_not_empty():
    """fake_phone 型態與內容非空（允許帶國碼/分機/破折號）"""
    val = fake_phone()
    assert isinstance(val, str)
    assert any(char.isdigit() for char in val)
    assert len(val) >= 8  # 只要求至少8字元，國際格式/分機不限制上限

def test_fake_address_type_and_not_empty():
    """fake_address 型態與非空"""
    val = fake_address()
    assert isinstance(val, str)
    assert val

def test_fake_user_complete_fields():
    """fake_user 五欄位皆存在且格式正確，phone 只驗證有數字且長度合理"""
    user = fake_user()
    assert set(user) == {"username", "password", "email", "phone", "address"}
    assert all(user.values())
    assert re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", user["email"])
    assert any(char.isdigit() for char in user["phone"])
    assert len(user["phone"]) >= 8

# ==== 產品相關 ====

def test_fake_product_id_is_uuid4():
    """fake_product_id 型態與 UUID4 格式"""
    val = fake_product_id()
    assert isinstance(val, str)
    assert re.match(r"^[0-9a-fA-F-]{36}$", val)

def test_fake_product_title_type_and_capitalized():
    """fake_product_title 型態與首字大寫"""
    val = fake_product_title()
    assert isinstance(val, str)
    assert val and val[0].isupper()

def test_fake_product_description_type_and_word_count():
    """fake_product_description 型態與單詞數量至少 3"""
    val = fake_product_description()
    assert isinstance(val, str)
    assert len(val.split()) >= 3   # Faker 可能小於 6，但 ≥3 保底合理


@pytest.mark.parametrize("min_price,max_price", [
    (1.0, 99.99),     # 預設正常區間
])
def test_fake_product_price_bounds_and_type(min_price, max_price):
    """fake_product_price 型態與正常區間，min<max（符合 faker 要求）"""
    price = fake_product_price(min_price, max_price)
    assert isinstance(price, float)
    assert min_price <= price <= max_price
    assert round(price, 2) == price

@pytest.mark.parametrize("min_price,max_price", [
    (0.01, 0.01),
    (10000, 10000),
])
def test_fake_product_price_min_eq_max_should_raise(min_price, max_price):
    """fake_product_price min=max 必須報 ValueError（與 faker 行為一致）"""
    with pytest.raises(ValueError):
        fake_product_price(min_price, max_price)

def test_fake_product_price_反向區間顛倒時必須報錯():
    """fake_product_price min>max 必須報 ValueError（與 faker 行為一致）"""
    min_price, max_price = 99.99, 1.0
    with pytest.raises(ValueError):
        fake_product_price(min_price, max_price)

def test_fake_product_complete_fields():
    """fake_product 欄位完整且格式正確"""
    prod = fake_product()
    assert set(prod) == {"id", "title", "description", "price"}
    assert re.match(r"^[0-9a-fA-F-]{36}$", prod["id"])
    assert prod["title"] and prod["title"][0].isupper()
    assert isinstance(prod["description"], str)
    assert isinstance(prod["price"], float)
    assert 1.0 <= prod["price"] <= 99.99

# ==== 購物車/訂單相關 ====

def test_fake_cart_quantity_in_range():
    """fake_cart_quantity 數值範圍與型態"""
    val = fake_cart_quantity()
    assert isinstance(val, int)
    assert 1 <= val <= 10

def test_fake_cart_date_default_format():
    """fake_cart_date 預設 yyyy-mm-dd 格式"""
    val = fake_cart_date()
    assert isinstance(val, str)
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", val)

def test_fake_cart_date_custom_format():
    """fake_cart_date 可自訂格式"""
    val = fake_cart_date(fmt="%Y%m%d")
    assert re.match(r"^\d{8}$", val)

def test_fake_order_id_is_uuid4():
    """fake_order_id 型態與 UUID4 格式"""
    val = fake_order_id()
    assert isinstance(val, str)
    assert re.match(r"^[0-9a-fA-F-]{36}$", val)

def test_fake_cart_complete_fields():
    """fake_cart 欄位完整與格式驗證"""
    cart = fake_cart()
    assert set(cart) == {"product", "quantity", "date", "order_id"}
    assert isinstance(cart["product"], dict)
    assert 1 <= cart["quantity"] <= 10
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", cart["date"])
    assert re.match(r"^[0-9a-fA-F-]{36}$", cart["order_id"])

# ==== 其他工具 ====

def test_fake_company_name_type_and_not_empty():
    """fake_company_name 型態與非空"""
    val = fake_company_name()
    assert isinstance(val, str)
    assert val

def test_fake_url_type_and_format():
    """fake_url 型態與基本格式（http/https）"""
    val = fake_url()
    assert isinstance(val, str)
    assert val.startswith("http")
