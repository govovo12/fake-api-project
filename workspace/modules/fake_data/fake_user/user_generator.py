from typing import Dict, Any, Tuple, Optional
from faker import Faker

from workspace.config.rules.error_codes import ResultCode

fake = Faker()

def generate_user_data() -> Tuple[bool, Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    測資產生器：建立假用戶資料（不包含 UUID）
    回傳格式：success, data, meta
    """
    try:
        name = fake.name()
        email = fake.email()
        password = fake.password(length=12, special_chars=True, digits=True, upper_case=True)

        return True, {
            "name": name,
            "email": email,
            "password": password,
            "passwordConfirm": password
        }, None

    except Exception as e:
        return False, None, {
            "code": ResultCode.FAKER_GENERATE_FAILED,
            "message": str(e),
        }
