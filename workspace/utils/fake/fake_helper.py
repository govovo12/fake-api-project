"""
fake_helper.py
測試用假資料產生工具（for unit/integration/fixture）
帳號、產品、購物車等常用資料一站式生成
"""

from typing import Dict, Any
from faker import Faker

faker = Faker()

# ==== 帳號相關 ====
def fake_username() -> str:
    """[TOOL] 隨機帳號名稱"""
    return faker.user_name()

def fake_password() -> str:
    """[TOOL] 隨機密碼"""
    return faker.password()

def fake_email() -> str:
    """[TOOL] 隨機 email"""
    return faker.email()

def fake_phone() -> str:
    """[TOOL] 隨機電話號碼（台灣格式）"""
    return faker.phone_number()

def fake_address() -> str:
    """[TOOL] 隨機地址"""
    return faker.address().replace('\n', ' ')

def fake_user() -> Dict[str, Any]:
    """[TOOL] 一組完整用戶資料 dict"""
    return {
        "username": fake_username(),
        "password": fake_password(),
        "email": fake_email(),
        "phone": fake_phone(),
        "address": fake_address(),
    }


# ==== 產品相關 ====
def fake_product_id() -> str:
    """[TOOL] 隨機產品 ID"""
    return faker.uuid4()

def fake_product_title() -> str:
    """[TOOL] 隨機產品名稱"""
    return faker.word().capitalize()

def fake_product_description() -> str:
    """[TOOL] 隨機產品描述"""
    return faker.sentence(nb_words=8)

def fake_product_price(min_price: float = 1.0, max_price: float = 99.99) -> float:
    """[TOOL] 隨機產品價格（可自訂範圍）"""
    return round(
        faker.pyfloat(
            left_digits=2,
            right_digits=2,
            positive=True,
            min_value=min_price,
            max_value=max_price
        ),
        2
    )

def fake_product() -> Dict[str, Any]:
    """[TOOL] 一組完整產品資料 dict"""
    return {
        "id": fake_product_id(),
        "title": fake_product_title(),
        "description": fake_product_description(),
        "price": fake_product_price(),
    }


# ==== 購物車/訂單相關 ====
def fake_cart_quantity() -> int:
    """[TOOL] 隨機購物車數量 1~10"""
    return faker.random_int(min=1, max=10)

def fake_cart_date(fmt: str = "%Y-%m-%d") -> str:
    """[TOOL] 隨機日期字串（可自訂格式）"""
    return faker.date(pattern=fmt)

def fake_order_id() -> str:
    """[TOOL] 隨機訂單 ID"""
    return faker.uuid4()

def fake_cart() -> Dict[str, Any]:
    """[TOOL] 一組購物車資料 dict"""
    return {
        "product": fake_product(),
        "quantity": fake_cart_quantity(),
        "date": fake_cart_date(),
        "order_id": fake_order_id(),
    }

# ==== 其他工具（可再擴充） ====
def fake_company_name() -> str:
    """[TOOL] 隨機公司名稱"""
    return faker.company()

def fake_url() -> str:
    """[TOOL] 隨機網址"""
    return faker.url()
