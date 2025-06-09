from typing import Dict, Any, Optional, Tuple
from faker import Faker
import random

from workspace.config.rules.error_codes import ResultCode
from workspace.config.envs.fake_product_config import CATEGORIES, CATEGORY_IMAGES

fake = Faker()
DEFAULT_IMAGE = "https://fakestoreapi.com/img/default.jpg"

def generate_product_data(
    title: Optional[str] = None,
    price: Optional[float] = None,
    description: Optional[str] = None,
    category: Optional[str] = None,
    image: Optional[str] = None
) -> Tuple[bool, Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    測資產生器：產生假商品資料（符合 Fake Store API 格式）
    - 可自訂傳入欄位參數以覆蓋預設值
    - 不包含 UUID（由組合器決定）
    回傳格式：success, data, meta
    """
    try:
        if not CATEGORIES:
            return False, None, {
                "code": ResultCode.PRODUCT_CATEGORY_EMPTY,
                "message": "CATEGORIES 配置為空，無法選擇商品分類"
            }

        selected_category = category or random.choice(CATEGORIES)

        data = {
            "title": title or fake.catch_phrase(),
            "price": price if price is not None else round(random.uniform(5, 500), 2),
            "description": description or fake.text(max_nb_chars=120),
            "category": selected_category,
            "image": image or CATEGORY_IMAGES.get(selected_category, DEFAULT_IMAGE)
        }

        return True, data, None

    except Exception as e:
        return False, None, {
            "code": ResultCode.PRODUCT_GENERATION_FAILED,
            "message": str(e)
        }
