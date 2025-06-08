class ResultCode:
    # 使用者測資相關錯誤碼
    USER_TESTDATA_SAVE_FAILED = 20103
    USER_TESTDATA_ALREADY_EXISTS = 20104
    USER_TESTDATA_FILE_WRITE_FAILED = 20105

    # 商品測資相關錯誤碼
    PRODUCT_TESTDATA_SAVE_FAILED = 30103
    PRODUCT_TESTDATA_ALREADY_EXISTS = 30104
    PRODUCT_TESTDATA_FILE_WRITE_FAILED = 30105

    # 資料夾建立錯誤
    TESTDATA_DIR_PREPARE_FAILED = 90105

    # 通用與流程成功
    SUCCESS = 0
    TESTDATA_GENERATION_SUCCESS = 10000


# ✅ 成功狀態碼集合（供 log_helper 判斷成功用）
SUCCESS_CODES = {
    ResultCode.SUCCESS,
    ResultCode.TESTDATA_GENERATION_SUCCESS,
}


# 錯誤原因對應表
REASON_CODE_MAP = {
    "file_exists": ResultCode.USER_TESTDATA_ALREADY_EXISTS,
    "mkdir_failed": ResultCode.TESTDATA_DIR_PREPARE_FAILED,
    "save_failed": ResultCode.USER_TESTDATA_FILE_WRITE_FAILED,
    "json_serialization_failed": ResultCode.USER_TESTDATA_FILE_WRITE_FAILED,
    "dir_not_found": ResultCode.USER_TESTDATA_SAVE_FAILED,
    "invalid_uuid": ResultCode.USER_TESTDATA_SAVE_FAILED,
    "not_a_dict": ResultCode.USER_TESTDATA_SAVE_FAILED,
    "file_not_found": ResultCode.USER_TESTDATA_FILE_WRITE_FAILED,
    "file_empty_or_invalid": ResultCode.USER_TESTDATA_FILE_WRITE_FAILED,
}

# 錯誤碼對應訊息表（供 log_helper 使用）
ERROR_CODE_MSG_MAP = {
    ResultCode.SUCCESS: "success",
    ResultCode.USER_TESTDATA_SAVE_FAILED: "無法儲存使用者測資",
    ResultCode.USER_TESTDATA_ALREADY_EXISTS: "使用者測資已存在",
    ResultCode.USER_TESTDATA_FILE_WRITE_FAILED: "寫入使用者測資失敗",
    ResultCode.PRODUCT_TESTDATA_SAVE_FAILED: "無法儲存商品測資",
    ResultCode.PRODUCT_TESTDATA_ALREADY_EXISTS: "商品測資已存在",
    ResultCode.PRODUCT_TESTDATA_FILE_WRITE_FAILED: "寫入商品測資失敗",
    ResultCode.TESTDATA_DIR_PREPARE_FAILED: "建立測資資料夾失敗",
    ResultCode.TESTDATA_GENERATION_SUCCESS: "測資產生任務完成",
}
