from faker import Faker
from workspace.config.rules.error_codes import ResultCode
import re

fake = Faker()

def generate_user_data(username=None, email=None, password=None) -> dict:
    """
    產生符合 Fake Store API 註冊格式的使用者資料。
    可傳入自定欄位（方便測試用），未提供的會自動產生。
    - 回傳 dict：成功資料
    - 回傳錯誤碼：欄位驗證失敗或錯誤
    """
    try:
        username = username or fake.name()
        email = email or fake.email()
        password = password or fake.password(length=12, special_chars=True, digits=True, upper_case=True)

        # 驗證邏輯
        if len(username) < 3 or len(username) > 50:
            return ResultCode.FAKER_GENERATE_FAILED

        if len(email) > 100 or not re.match(r"^[^@]+@[^@]+\.[^@]+", email):
            return ResultCode.FAKER_GENERATE_FAILED

        if len(password) < 8 or len(password) > 16:
            return ResultCode.FAKER_GENERATE_FAILED

        return {
            "username": username,
            "email": email,
            "password": password,
        }

    except Exception:
        return ResultCode.FAKER_GENERATE_FAILED
