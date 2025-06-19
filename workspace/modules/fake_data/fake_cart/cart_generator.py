import random
from datetime import datetime, timedelta


def generate_cart_data() -> dict:
    """
    產生購物車測試資料：
    - userId：1～10 的隨機整數
    - date：今日或過去 7 天內任一天
    - products：1～5 筆商品，每筆含隨機 productId 與數量（不重複）
    """
    user_id = random.randint(1, 10)
    date = (datetime.today() - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d")

    product_count = random.randint(1, 5)
    used_ids = set()
    products = []

    while len(products) < product_count:
        product_id = random.randint(1, 20)
        if product_id in used_ids:
            continue
        used_ids.add(product_id)
        products.append({
            "productId": product_id,
            "quantity": random.randint(1, 5)
        })

    cart_data = {
        "userId": user_id,
        "date": date,
        "products": products
}

   

    return cart_data
