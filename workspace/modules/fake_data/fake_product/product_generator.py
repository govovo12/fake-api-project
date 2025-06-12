import random
import string
from workspace.config.rules.error_codes import ResultCode

# 預設商品類別清單
CATEGORY_LIST = [
    "Clothes",
    "Electronics",
    "Jewelery",
    "Men's Clothing",
    "Women's Clothing"
]

def generate_product_data(title=None, price=None, category=None, image=None):
    """
    產生商品測試資料，並符合 Fake Store API 的要求。
    隨機生成 description 和 image，並驗證格式是否正確。
    """
    try:
        # 每次都從類別清單中隨機選一個，不管外部有沒有傳 category
        category = random.choice(CATEGORY_LIST)  # 隨機選擇一個 category
        # ✅ 檢查選擇的 category 是否在 CATEGORY_LIST 內
        if category not in CATEGORY_LIST:
            return ResultCode.PRODUCT_CATEGORY_EMPTY  # 如果選擇的 category 不在清單內，返回錯誤碼

        # ✅ 檢查 price 是否為數字
        if price is not None and not isinstance(price, (int, float)):
            return ResultCode.PRODUCT_GENERATION_FAILED  # 如果 price 不是數字，返回錯誤碼

        # 隨機生成 description（長度 5 至 10，字母 + 數字）
        description = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(5, 10)))

        # 如果 description 不符合要求（例如長度不對），返回錯誤碼
        if len(description) < 5 or len(description) > 10:
            return ResultCode.PRODUCT_GENERATION_FAILED  # 如果 description 格式錯誤，返回錯誤碼

        # 固定的圖片 URL
        image = "https://fakeimg.pl/250x250/?text=Sample"

        # 檢查 image 是否為空
        if not image:
            return ResultCode.PRODUCT_GENERATION_FAILED  # 如果 image 為空，返回錯誤碼

        # 生成商品資料並返回
        return {
            "title": title or "Random Product",
            "price": price or round(random.uniform(5.0, 500.0), 2),
            "description": description,
            "image": image,
            "category": category
        }

    except Exception:
        return ResultCode.PRODUCT_GENERATION_FAILED  # 發生其他錯誤時返回錯誤碼
