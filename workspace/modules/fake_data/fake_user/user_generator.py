from faker import Faker
from workspace.config.rules.error_codes import ResultCode
import re

fake = Faker()

def generate_user_data(name=None, email=None, password=None) -> dict:
    """
    生成符合註冊規範的用戶資料。若提供參數會覆蓋預設生成值（供測試用）。
    成功時回傳 dict，若任一欄位驗證失敗則回傳錯誤碼。
    """
    try:
        name = name or fake.name()
        email = email or fake.email()
        password = password or fake.password(length=12, special_chars=True, digits=True, upper_case=True)

        # 驗證邏輯
        if len(name) < 3 or len(name) > 50:
            return ResultCode.FAKER_GENERATE_FAILED

        if len(email) > 100 or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return ResultCode.FAKER_GENERATE_FAILED

        if len(password) < 8 or len(password) > 16:
            return ResultCode.FAKER_GENERATE_FAILED

        return {
            "name": name,
            "email": email,
            "password": password
        }

    except Exception as e:
        # 捕捉其他錯誤並返回通用錯誤碼
        return ResultCode.FAKER_GENERATE_FAILED
