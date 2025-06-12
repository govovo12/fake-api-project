from workspace.config.rules.error_codes import ResultCode
from workspace.utils.file.file_helper import ensure_dir, ensure_file
from workspace.utils.data.data_loader import save_json
from workspace.modules.fake_data.fake_product.product_generator import generate_product_data
from workspace.config.paths import get_product_path

def build_product_data_and_write(uuid: str) -> int:
    """
    組合器：根據 uuid 建立 product 測資檔案流程
    1. 取得路徑
    2. 建資料夾
    3. 建空檔案
    4. 產測資
    5. 寫入測資
    6. 回傳錯誤碼
    """
    path = get_product_path(uuid)

    # 1. 建立資料夾
    code = ensure_dir(path.parent)
    if code != ResultCode.SUCCESS:
        return code

    # 2. 建立空檔案（如果不存在）
    code = ensure_file(path)
    if code != ResultCode.SUCCESS:
        return code

    # 3. 產生測資
    data = generate_product_data()
    if not isinstance(data, dict):
        return data  # 錯誤碼由任務模組回傳

    # 4. 寫入檔案
    code = save_json(path, data)
    return code  # 成功或錯誤碼
