# ----------------------------------------
# 📦 標準函式庫
# ----------------------------------------
import random
import string

# ----------------------------------------
# 🛠️ 專案內部錯誤碼與設定
# ----------------------------------------
from workspace.config.rules.error_codes import ResultCode
from workspace.config.envs.fake_product_config import CATEGORIES, CATEGORY_IMAGES


def generate_product_data(title=None, price=None, category=None, image=None) -> dict:
    """
    任務模組：產生符合 Fake Store API 格式的商品測試資料

    - 若未提供 image，會根據分類補預設圖片
    - image 若為空字串，視為錯誤
    - 欄位驗證失敗時回傳錯誤碼

    :param title: 自訂標題（選填）
    :param price: 自訂價格（選填）
    :param category: 自訂分類（選填，若無則隨機）
    :param image: 自訂圖片（選填，空字串視為錯）
    :return: dict 商品資料 或錯誤碼
    """
    try:
        # 分類處理
        category = category or random.choice(CATEGORIES)
        if category not in CATEGORIES:
            return ResultCode.PRODUCT_CATEGORY_EMPTY

        # 價格驗證
        if price is not None and not isinstance(price, (int, float)):
            return ResultCode.PRODUCT_GENERATION_FAILED

        # 描述產生
        description = ''.join(random.choices(
            string.ascii_lowercase + string.digits,
            k=random.randint(5, 10)
        ))
        if len(description) < 5 or len(description) > 10:
            return ResultCode.PRODUCT_GENERATION_FAILED

        # ✅ image 邏輯處理
        if image == "":
            return ResultCode.PRODUCT_GENERATION_FAILED  # 空字串為無效輸入

        if not image:
            image = CATEGORY_IMAGES.get(category)  # 根據分類補圖

        if not image:
            return ResultCode.PRODUCT_GENERATION_FAILED  # 若分類無對應圖也失敗

        return {
            "title": title or "Random Product",
            "price": price or round(random.uniform(5.0, 500.0), 2),
            "description": description,
            "image": image,
            "category": category
        }

    except Exception:
        return ResultCode.PRODUCT_GENERATION_FAILED
