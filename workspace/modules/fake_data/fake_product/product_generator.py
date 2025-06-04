# fake_product/product_generator.py

from typing import Dict, Any, Optional
from faker import Faker
import random

# ✅ 從資料層讀取分類與圖片設定
from workspace.config.envs.fake_product_config import CATEGORIES, CATEGORY_IMAGES

fake = Faker()

DEFAULT_IMAGE = "https://fakestoreapi.com/img/default.jpg"

def generate_product_data(
    title: Optional[str] = None,
    price: Optional[float] = None,
    description: Optional[str] = None,
    category: Optional[str] = None,
    image: Optional[str] = None
) -> Dict[str, Any]:
    """
    產生符合 Fake Store API 的假商品資料，可自訂或隨機欄位。
    分類與圖片來自設定檔。
    """
    selected_category = category or random.choice(CATEGORIES)

    return {
        "title": title or fake.catch_phrase(),
        "price": price if price is not None else round(random.uniform(5, 500), 2),
        "description": description or fake.text(max_nb_chars=120),
        "category": selected_category,
        "image": image or CATEGORY_IMAGES.get(selected_category, DEFAULT_IMAGE)
    }
