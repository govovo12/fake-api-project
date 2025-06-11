from typing import Optional
from workspace.utils.file.file_helper import file_exists, generate_testdata_path, ensure_dir
from workspace.utils.data.data_initializer import write_empty_data_file
from workspace.utils.retry.retry_handler import safe_call
from workspace.config.rules.error_codes import ResultCode


def prepare_testdata_files(uuid: str) -> Optional[int]:
    """
    檢查並建立空白測資檔案（user / product）
    成功 → 無回傳  
    失敗 → 回傳錯誤碼（ResultCode）
    """
    def should_retry(code: int) -> bool:
        """
        判斷哪些錯誤碼可以 retry（transient error）
        """
        return code in {
            ResultCode.FILE_WRITE_FAILED,
            ResultCode.FILE_SERIALIZATION_FAILED,
            ResultCode.UNKNOWN_FILE_SAVE_ERROR,
        }

    try:
        # Step 1: 路徑產生（驗證 UUID 合法性）
        user_path = generate_testdata_path("user", uuid)
        product_path = generate_testdata_path("product", uuid)

        # 確保資料夾存在
        ensure_dir(user_path.parent)  # 確保資料夾存在
        ensure_dir(product_path.parent)

        # Step 2: 檢查是否已存在
        if file_exists(user_path) or file_exists(product_path):
            return ResultCode.USER_TESTDATA_ALREADY_EXISTS

        # Step 3: 建立空白 user 測資檔
        code = safe_call(write_empty_data_file, user_path, "user", max_retries=1, retry_on=should_retry)
        if code is not None:
            return code  # 返回錯誤碼

        # Step 4: 建立空白 product 測資檔
        code = safe_call(write_empty_data_file, product_path, "product", max_retries=1, retry_on=should_retry)
        if code is not None:
            return code  # 返回錯誤碼

        return ResultCode.SUCCESS  # 成功返回 0

    except Exception as e:
        print(f"[DEBUG] prepare_testdata_files 例外：{type(e).__name__} - {str(e)}")
        return ResultCode.UNKNOWN_FILE_SAVE_ERROR  # 發生異常返回未知錯誤碼
