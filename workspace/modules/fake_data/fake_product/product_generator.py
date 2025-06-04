# fake_product/product_generator.py

from typing import Dict, Any, Optional, Tuple
from faker import Faker
import random

from workspace.config.envs.fake_product_config import CATEGORIES, CATEGORY_IMAGES
from workspace.config.rules.error_codes import ResultCode

fake = Faker()
DEFAULT_IMAGE = "https://fakestoreapi.com/img/default.jpg"

def generate_product_data(
    title: Optional[str] = None,
    price: Optional[float] = None,
    description: Optional[str] = None,
    category: Optional[str] = None,
    image: Optional[str] = None
) -> Tuple[int, Optional[Dict[str, Any]]]:
    """
    產生符合 Fake Store API 的假商品資料，回傳 (錯誤碼, 資料 dict)
    """
    if not CATEGORIES:
        return ResultCode.PRODUCT_GEN_FAIL, None

    selected_category = category or random.choice(CATEGORIES)

    data = {
        "title": title or fake.catch_phrase(),
        "price": price if price is not None else round(random.uniform(5, 500), 2),
        "description": description or fake.text(max_nb_chars=120),
        "category": selected_category,
        "image": image or CATEGORY_IMAGES.get(selected_category, DEFAULT_IMAGE)
    }

    return ResultCode.SUCCESS, data
