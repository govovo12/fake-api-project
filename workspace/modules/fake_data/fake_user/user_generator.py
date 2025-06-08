from typing import Dict, Any, Tuple, Optional
from faker import Faker
import uuid
from workspace.config.rules.error_codes import ResultCode

fake = Faker()

def generate_user_data() -> Tuple[int, Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    建立假用戶資料。回傳三值：錯誤碼、資料 dict、錯誤 meta
    """
    try:
        name = fake.name()
        unique_id = uuid.uuid4().hex[:8]
        email = f"user_{unique_id}@mail.com"
        password = fake.password(length=12, special_chars=True, digits=True, upper_case=True)

        return ResultCode.SUCCESS, {
            "name": name,
            "email": email,
            "password": password,
            "passwordConfirm": password
        }, None

    except Exception as e:
        return ResultCode.USER_GENERATION_FAILED, None, {
            "step": "generate_user_data",
            "reason": "faker_error",
            "message": str(e)
        }
