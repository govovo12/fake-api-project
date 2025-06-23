# ----------------------------------------
# 📦 錯誤碼與路徑設定
# ----------------------------------------
from workspace.config.rules.error_codes import ResultCode
from workspace.config.paths import get_cart_path

# ----------------------------------------
# 🛠️ 工具模組
# ----------------------------------------
from workspace.utils.file.file_helper import ensure_dir, ensure_file
from workspace.utils.data.data_loader import save_json

# ----------------------------------------
# 🧩 任務模組（購物車測資產生器）
# ----------------------------------------
from workspace.modules.fake_data.fake_cart.cart_generator import generate_cart_data


def build_cart_data_and_write(uuid: str) -> int:
    """
    組合器：根據指定 uuid 建立購物車測資 JSON 檔案

    流程：
    1. 取得購物車資料存放路徑
    2. 建立資料夾與空檔案
    3. 呼叫購物車測資產生器
    4. 寫入 JSON 檔案
    5. 回傳成功或錯誤碼
    """
    path = get_cart_path(uuid)

    # 1. 建立資料夾
    code = ensure_dir(path.parent)
    if code != ResultCode.SUCCESS:
        return code

    # 2. 建立空檔案（如尚未存在）
    code = ensure_file(path)
    if code != ResultCode.SUCCESS:
        return code

    # 3. 產生購物車測資內容
    cart_data = generate_cart_data()
    if not isinstance(cart_data, dict):
        return ResultCode.CART_GENERATION_FAILED  # 非 dict 回傳錯誤碼

    # 4. 寫入 JSON 檔案
    code = save_json(path, cart_data)
    return code  # 回傳成功或錯誤碼
