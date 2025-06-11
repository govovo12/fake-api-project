from typing import Dict, Any
from faker import Faker
from workspace.config.rules.error_codes import ResultCode, TaskModuleError

fake = Faker()

def generate_user_data() -> Dict[str, Any]:
    """
    任務模組：產生假用戶測試資料（符合 Fake Store API 註冊 API 格式）
    """
    try:
        # 產生隨機的姓名、信箱和密碼
        name = fake.name()
        email = fake.email()
        password = fake.password(length=12, special_chars=True, digits=True, upper_case=True)

        user_data = {
            "name": name,
            "email": email,
            "password": password
        }
        
        # 打印出生成的用戶資料以進行檢查
        print(f"Generated user data: {user_data}")
        return user_data

    except Exception:
        raise TaskModuleError(ResultCode.FAKER_GENERATE_FAILED)


        