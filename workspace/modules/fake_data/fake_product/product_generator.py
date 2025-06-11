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
    category: Optional[str] = None
) -> Dict[str, Any]:
    """
    任務模組：產生假商品測試資料（符合 Fake Store API 建立商品 API 格式）
    """
    try:
        print(f"[DEBUG] CATEGORIES: {CATEGORIES}")  # 查看 CATEGORIES 的內容
        if not CATEGORIES:
            raise TaskModuleError(ResultCode.PRODUCT_CATEGORY_EMPTY)

        selected_category = category or random.choice(CATEGORIES)
        print(f"[DEBUG] Selected Category: {selected_category}")  # 確認選擇的商品分類

        product_data = {
            "title": title or fake.catch_phrase(),
            "price": price if price is not None else round(random.uniform(5, 500), 2),
            "category": selected_category
        }

        # 打印生成的商品資料
        print(f"[DEBUG] Generated product data: {product_data}")
        return product_data

    except Exception:
        raise TaskModuleError(ResultCode.PRODUCT_GENERATION_FAILED)


