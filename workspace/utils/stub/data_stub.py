from datetime import date

def stub_user_payload(username="johnd", password="m38rmF$"):
    return {
        "username": username,
        "password": password
    }

def stub_cart_payload(user_id=3, cart_date="2020-03-01", products=None):
    return {
        "userId": user_id,
        "date": cart_date,
        "products": products or [
            {"productId": 1, "quantity": 4},
            {"productId": 2, "quantity": 1},
            {"productId": 3, "quantity": 6}
        ]
    }
