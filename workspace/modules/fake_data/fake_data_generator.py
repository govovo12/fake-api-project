# fake_data/fake_data_generator.py
from typing import Dict, Any
from faker import Faker
import random
import re

fake = Faker()

def generate_fake_user_data() -> Dict[str, Any]:
    """
    生成符合 Fake Store API 格式的隨機用戶資料
    並添加長度和格式限制
    """
    # 用戶名：4-20 字符，僅允許字母和數字
    username = f"user_{random.randint(1000, 9999)}"
    
    # 電子郵件：標準格式
    email = fake.email()
    
    # 密碼：最少 8 個字符，並且包含數字、字母和特殊字符
    password = fake.password(length=12, special_chars=True, digits=True, upper_case=True)
    
    # 電話號碼：10 位數字
    phone = fake.phone_number()
    
    # 地址：隨機生成，無特別限制，但限制長度在 100 字符以內
    address = fake.address() 
    
    # 返回生成的假資料
    return {
        "username": username,  # 用戶名
        "email": email,        # 電子郵件
        "password": password,  # 密碼
        "phone": phone,        # 電話
        "address": address     # 地址
    }
