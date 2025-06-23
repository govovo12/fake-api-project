# ----------------------------------------
# 📦 標準函式庫
# ----------------------------------------
import random
from datetime import datetime, timedelta


def generate_cart_data() -> dict:
    """
    任務模組：產生購物車測試資料（符合 Fake Store API 結構）

    - userId：1～10 的隨機整數
    - date：今日或過去 7 天內的任一天
    - products：1～5 筆商品，每筆含隨機不重複的 productId 與數量

    :return: dict 組成的購物車資料
    """
    # 隨機指定使用者 ID 與購物日期
    user_id = random.randint(1, 10)
    date = (datetime.today() - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d")

    # 準備 1～5 筆商品，每筆含唯一 productId
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

    return {
        "userId": user_id,
        "date": date,
        "products": products
    }
