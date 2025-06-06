def build_register_payload(user_data: dict) -> dict:
    if not user_data:
        return {}

    payload = {
        "username": user_data.get("username"),
        "password": user_data.get("password"),
        "email": user_data.get("email"),
        "phone": user_data.get("phone"),
        "uuid": user_data.get("uuid"),
        # 可依照實際 API 補上其他欄位
    }

    return payload
