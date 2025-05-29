from workspace.utils.stub.data_stub import stub_user_payload, stub_cart_payload


def get_valid_user_cart_payload():
    """
    回傳一組有效用戶登入資訊 + 對應購物車資料
    適用於一般購物流程測試。
    """
    return {
        "user": stub_user_payload(),
        "cart": stub_cart_payload()
    }


def get_valid_user_only():
    """
    回傳一組有效用戶登入資料（不含購物車）
    適用於登入測試或登入失敗情境前置。
    """
    return stub_user_payload()


def get_cart_only(user_id=3):
    """
    回傳一組購物車資料，預設 user_id 為 3
    可作為已登入狀態後測試購物車模組使用。
    """
    return stub_cart_payload(user_id=user_id)
