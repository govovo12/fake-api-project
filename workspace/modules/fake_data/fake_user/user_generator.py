# fake_user/user_generator.py
from typing import Dict, Any, Tuple
from faker import Faker
import uuid

from workspace.config.rules import error_codes

fake = Faker()

def generate_user_data() -> Tuple[int, Dict[str, Any]]:
    """
    產生符合 Fake Store API 註冊格式的假用戶資料。
    回傳 (錯誤碼, 資料)，若成功錯誤碼為 0，否則對應錯誤碼。
    """
    try:
        name = fake.name()
        unique_id = uuid.uuid4().hex[:8]
        email = f"user_{unique_id}@mail.com"
        password = fake.password(length=12, special_chars=True, digits=True, upper_case=True)

        return 0, {
            "name": name,
            "email": email,
            "password": password,
            "passwordConfirm": password
        }

    except Exception:
        return error_codes.ACCOUNT_GEN_FAIL, {}
