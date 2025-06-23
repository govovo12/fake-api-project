# ----------------------------------------
# 📦 錯誤碼與路徑設定
# ----------------------------------------
from workspace.config.rules.error_codes import ResultCode
from workspace.config.paths import get_product_path

# ----------------------------------------
# 🛠️ 工具模組
# ----------------------------------------
from workspace.utils.file.file_helper import ensure_dir, ensure_file
from workspace.utils.data.data_loader import save_json

# ----------------------------------------
# 🧩 任務模組（商品測資產生器）
# ----------------------------------------
from workspace.modules.fake_data.fake_product.product_generator import generate_product_data


def build_product_data_and_write(uuid: str) -> int:
    """
    組合器：根據指定 uuid 建立商品測資 JSON 檔案

    流程：
    1. 取得商品資料存放路徑
    2. 建立資料夾與空檔案
    3. 呼叫商品測資產生器
    4. 寫入 JSON 檔案
    5. 回傳成功或錯誤碼
    """
    path = get_product_path(uuid)

    # 1. 建立資料夾
    code = ensure_dir(path.parent)
    if code != ResultCode.SUCCESS:
        return code

    # 2. 建立空檔案（如尚未存在）
    code = ensure_file(path)
    if code != ResultCode.SUCCESS:
        return code

    # 3. 產生商品測資內容
    data = generate_product_data()
    if not isinstance(data, dict):
        return data  # 任務模組會回傳錯誤碼

    # 4. 寫入 JSON 檔案
    code = save_json(path, data)
    return code  # 回傳成功或錯誤碼
