from typing import Tuple, Optional
from pathlib import Path

from workspace.utils.file.file_helper import (
    file_exists,
    generate_testdata_path
)
from workspace.utils.data.data_initializer import write_empty_data_file
from workspace.config.rules.error_codes import ResultCode, REASON_CODE_MAP


def prepare_testdata_files(uuid: str) -> Tuple[int, Optional[dict], Optional[dict]]:
    """
    檢查並建立空白測資檔案（user / product）
    """
    user_path, meta_u = generate_testdata_path("user", uuid)
    product_path, meta_p = generate_testdata_path("product", uuid)

    # 如果路徑生成失敗（格式錯誤）
    if not user_path:
        code = REASON_CODE_MAP.get(meta_u.get("reason", ""), ResultCode.USER_TESTDATA_FILE_WRITE_FAILED)
        return code, None, meta_u
    if not product_path:
        code = REASON_CODE_MAP.get(meta_p.get("reason", ""), ResultCode.TESTDATA_PRODUCT_FILE_WRITE_FAILED)
        return code, None, meta_p

    # 檢查是否已存在
    if file_exists(user_path) or file_exists(product_path):
        return REASON_CODE_MAP.get("file_already_exists", ResultCode.USER_TESTDATA_ALREADY_EXISTS), None, {
            "reason": "file_already_exists",
            "user_path": str(user_path),
            "product_path": str(product_path),
        }

    # 建立 user 測資檔
    success_u, meta_u = write_empty_data_file(user_path, "user")
    if not success_u:
        reason = meta_u.get("reason", "")
        code = REASON_CODE_MAP.get(reason, ResultCode.TESTDATA_USER_FILE_WRITE_FAILED)
        return code, None, meta_u

    # 建立 product 測資檔
    success_p, meta_p = write_empty_data_file(product_path, "product")
    if not success_p:
        reason = meta_p.get("reason", "")
        code = REASON_CODE_MAP.get(reason, ResultCode.TESTDATA_PRODUCT_FILE_WRITE_FAILED)
        return code, None, meta_p

    return ResultCode.SUCCESS, {
        "user_path": str(user_path),
        "product_path": str(product_path)
    }, None
