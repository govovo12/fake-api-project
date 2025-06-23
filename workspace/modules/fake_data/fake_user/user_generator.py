# ----------------------------------------
# 📦 第三方套件
# ----------------------------------------
from faker import Faker
import re

# ----------------------------------------
# 🛠️ 專案內部錯誤碼
# ----------------------------------------
from workspace.config.rules.error_codes import ResultCode

fake = Faker()


def generate_user_data(uuid: str = None, username=None, email=None, password=None) -> dict:
    """
    任務模組：產生符合 Fake Store API 註冊格式的使用者資料

    - 可傳入自訂欄位，未指定的將自動產生（方便測試覆蓋）
    - 若有傳入 uuid，會將其前 8 碼加進 username 與 email，避免重複
    - 若欄位格式驗證失敗，回傳錯誤碼（ResultCode.FAKER_GENERATE_FAILED）

    :param uuid: 選填，作為識別碼加入帳號與 email
    :param username: 自訂帳號（選填）
    :param email: 自訂信箱（選填）
    :param password: 自訂密碼（選填）
    :return: dict 成功資料 或 ResultCode 錯誤碼
    """
    try:
        suffix = uuid[:8] if uuid else fake.uuid4()[:8]

        username = username or f"tester_{suffix}"
        email = email or f"user_{suffix}@example.com"
        password = password or fake.password(length=12, special_chars=True, digits=True, upper_case=True)

        # ✅ 格式驗證
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
