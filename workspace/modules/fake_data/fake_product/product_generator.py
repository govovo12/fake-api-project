from typing import Dict, Any, Optional
from faker import Faker
import random

from workspace.config.rules.error_codes import ResultCode, TaskModuleError
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
    任務模組：產生假商品測試資料（符合 Fake Store API 格式）
    - 可自訂傳入欄位參數以覆蓋預設值
    - 若 CATEGORIES 配置為空，拋出錯誤
    - 成功時回傳 dict，失敗拋出 TaskModuleError
    """
    try:
        if not CATEGORIES:
            raise TaskModuleError(ResultCode.PRODUCT_CATEGORY_EMPTY)

        selected_category = category or random.choice(CATEGORIES)

        return {
            "title": title or fake.catch_phrase(),
            "price": price if price is not None else round(random.uniform(5, 500), 2),
            "description": description or fake.text(max_nb_chars=120),
            "category": selected_category,
            "image": image or CATEGORY_IMAGES.get(selected_category, DEFAULT_IMAGE)
        }

    except Exception:
        raise TaskModuleError(ResultCode.PRODUCT_GENERATION_FAILED)
