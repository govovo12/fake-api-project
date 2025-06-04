# fake_user/user_generator.py
from typing import Dict, Any
from faker import Faker
import uuid

fake = Faker()

def generate_fake_user_data() -> Dict[str, Any]:
    """
    產生符合 Fake Store API 註冊格式的假用戶資料。
    重點強化 email 與 password 的隨機性，避免重複。
    """

    # ✅ 使用 faker 隨機產生名字
    name = fake.name()

    # ✅ 使用 uuid 加強 email 唯一性（例如：user_a7c8b2d1@mail.com）
    unique_id = uuid.uuid4().hex[:8]
    email = f"user_{unique_id}@mail.com"

    # ✅ 高強度隨機密碼，長度 12 位、包含特殊字元、大寫與數字
    password = fake.password(length=12, special_chars=True, digits=True, upper_case=True)

    return {
        "name": name,
        "email": email,
        "password": password,
        "passwordConfirm": password
    }
