from utils.stub.data_stub import (
    stub_valid_user_json,
    stub_user_payload,
    stub_cart_payload,
)

def get_valid_user_cart_payload():
    """
    取得完整使用者與購物車假資料，且 user 必須含 username 欄位
    """
    user = stub_valid_user_json()
    # 兼容測試需求：如果 user 裡沒 username，加上預設
    if "username" not in user:
        user["username"] = "default_username"
    cart = stub_cart_payload()
    return {
        "user": user,
        "cart": cart,
    }

def get_valid_user_only():
    """
    取得只有使用者資料的假資料
    """
    return stub_user_payload()

def get_cart_only(user_id=None):
    """
    取得購物車資料，可指定 user_id
    """
    cart = stub_cart_payload()
    if user_id is not None:
        cart["userId"] = user_id
    return cart
