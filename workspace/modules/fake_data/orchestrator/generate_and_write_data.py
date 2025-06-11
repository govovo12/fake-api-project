from workspace.modules.fake_data.fake_product.product_generator import generate_product_data
from workspace.modules.fake_data.fake_user.user_generator import generate_user_data
from workspace.utils.retry.retry_handler import safe_call
from workspace.utils.file.file_helper import save_json, generate_testdata_path, ensure_dir  # 確保引入 ensure_dir
from workspace.config.rules.error_codes import ResultCode
from typing import Optional

def generate_and_write_data(data_type: str, uuid: str) -> Optional[int]:
    """
    生成並寫入資料檔案（商品資料 / 使用者資料）
    - 根據 `data_type` 呼叫對應的生成器，並儲存資料到對應的檔案
    """
    try:
        # 根據 data_type 生成資料
        if data_type == "user":
            data = safe_call(generate_user_data)  # 生成使用者資料
        elif data_type == "product":
            data = safe_call(generate_product_data)  # 生成商品資料
        else:
            return ResultCode.UNKNOWN_FILE_SAVE_ERROR  # 無效的類型

        if data is None or not data:
            return ResultCode.DATA_GENERATION_FAILED  # 資料生成失敗，空的資料

        # 將資料寫入檔案
        path = generate_testdata_path(data_type, uuid)
        
        # 確保資料夾存在
        ensure_dir(path.parent)  # 確保資料夾存在
        
        # 儲存資料
        code = safe_call(save_json, path, data)
        if code is not None:
            return code

        return ResultCode.SUCCESS  # 成功

    except Exception as e:
        print(f"[DEBUG] generate_and_write_data 例外：{type(e).__name__} - {str(e)}")
        return ResultCode.UNKNOWN_FILE_SAVE_ERROR  # 發生異常返回錯誤碼
