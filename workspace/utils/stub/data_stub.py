from pathlib import Path
from datetime import date

def tool(func):
    func.is_tool = True
    return func

@tool
def stub_shiftjis_encoded_json() -> bytes:
    """回傳 Shift-JIS 編碼的假 JSON 資料 (格式測試用) [TOOL]"""
    return '{"key": "value"}'.encode("shift_jis")

@tool
def stub_valid_user_json() -> dict:
    """產生範例使用者 dict [TOOL]"""
    return {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com"
    }

@tool
def stub_product_payload(product_id=101, quantity=1):
    """產生範例商品 payload dict [TOOL]"""
    return {
        "product_id": product_id,
        "quantity": quantity
    }

@tool
def stub_nonexistent_path() -> Path:
    """回傳一個一定不存在的檔案路徑 [TOOL]"""
    return Path("Z:/this/path/should/not/exist.json")

@tool
def stub_invalid_json_file(tmp_path: Path) -> Path:
    """建立一個格式錯誤的 JSON 檔案並回傳其路徑 [TOOL]"""
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{bad json}", encoding="utf-8")
    return bad_file

@tool
def stub_user_payload(username="johnd", password="m38rmF$"):
    """產生登入用戶 payload dict [TOOL]"""
    return {
        "username": username,
        "password": password
    }

@tool
def stub_cart_payload(user_id=3, cart_date="2020-03-01", products=None):
    """產生購物車 payload dict [TOOL]"""
    return {
        "userId": user_id,
        "date": cart_date,
        "products": products or [
            {"productId": 1, "quantity": 4},
            {"productId": 2, "quantity": 1},
            {"productId": 3, "quantity": 6}
        ]
    }
