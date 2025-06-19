from workspace.config.rules.error_codes import ResultCode
from workspace.config.paths import get_cart_path
from workspace.utils.file.file_helper import ensure_dir, ensure_file
from workspace.utils.data.data_loader import save_json
from workspace.modules.fake_data.fake_cart.cart_generator import generate_cart_data


def build_cart_data_and_write(uuid: str) -> int:
    """
    建立購物車測資檔案（根據 uuid）
    - 建立路徑
    - 呼叫產生器
    - 寫入 JSON 檔案
    - 回傳成功或錯誤碼
    """
    path = get_cart_path(uuid)

    # 建立資料夾與空檔案
    code = ensure_dir(path.parent)
    if code != ResultCode.SUCCESS:
        return code

    code = ensure_file(path)
    if code != ResultCode.SUCCESS:
        return code

    # 產生測資資料
    cart_data = generate_cart_data()
    if not isinstance(cart_data, dict):
        return ResultCode.CART_GENERATION_FAILED

    # 寫入 JSON 檔案
    code = save_json(path, cart_data)
    return code
