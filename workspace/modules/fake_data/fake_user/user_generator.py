from typing import Dict, Any
from faker import Faker
from workspace.config.rules.error_codes import ResultCode, TaskModuleError

fake = Faker()


def generate_user_data() -> Dict[str, Any]:
    """
    任務模組：產生假用戶測試資料（不包含 UUID）
    - 使用 Faker 模擬姓名、信箱與密碼格式
    - 成功時回傳 dict 結構，失敗拋出 TaskModuleError
    """
    try:
        name = fake.name()
        email = fake.email()
        password = fake.password(length=12, special_chars=True, digits=True, upper_case=True)

        return {
            "name": name,
            "email": email,
            "password": password,
            "passwordConfirm": password
        }

    except Exception:
        raise TaskModuleError(ResultCode.FAKER_GENERATE_FAILED)
