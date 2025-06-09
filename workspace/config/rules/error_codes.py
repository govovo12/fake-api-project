class ResultCode:
    # 使用者測資相關錯誤碼
    USER_TESTDATA_SAVE_FAILED = 20103
    USER_TESTDATA_ALREADY_EXISTS = 20104
    USER_TESTDATA_FILE_WRITE_FAILED = 20105
    USER_UUID_ATTACH_FAILED = 20106

    # 商品測資相關錯誤碼
    PRODUCT_TESTDATA_SAVE_FAILED = 30103
    PRODUCT_TESTDATA_ALREADY_EXISTS = 30104
    PRODUCT_TESTDATA_FILE_WRITE_FAILED = 30105
    PRODUCT_UUID_ATTACH_FAILED = 30106
    PRODUCT_GENERATION_FAILED = 30107  


    # UUID 錯誤
    UUID_GEN_FAIL = 40101

    # 資料夾建立錯誤
    TESTDATA_DIR_PREPARE_FAILED = 90105

    # 通用與流程成功
    SUCCESS = 0
    TESTDATA_GENERATION_SUCCESS = 10000
   
    # 通用 I/O 錯誤碼
    FILE_NOT_FOUND = 80001
    FILE_LOAD_FAILED = 80002
    FILE_WRITE_FAILED = 80003
    FILE_PERMISSION_DENIED = 80004
    FILE_ENCODING_ERROR = 80005
    FILE_PATH_GENERATION_FAILED = 80006
    FILE_SERIALIZATION_FAILED = 80007
    INVALID_FILE_DATA = 80008
    UNKNOWN_FILE_SAVE_ERROR = 80009

    # 資料驗證錯誤碼
    UUID_FORMAT_INVALID = 81001
    INVALID_FILE_KIND = 81002
    INVALID_DATA_TYPE = 81003
    ENRICH_UUID_FAILED = 81004
    


# ✅ 成功狀態碼集合（供 log_helper 判斷成功用）
SUCCESS_CODES = {
    ResultCode.SUCCESS,
    ResultCode.TESTDATA_GENERATION_SUCCESS,
}


# 錯誤原因對應表
REASON_CODE_MAP = {
    # 共用
    "file_exists": ResultCode.USER_TESTDATA_ALREADY_EXISTS,
    "mkdir_failed": ResultCode.TESTDATA_DIR_PREPARE_FAILED,

    # 使用者
    "save_failed_user": ResultCode.USER_TESTDATA_FILE_WRITE_FAILED,
    "json_serialization_failed_user": ResultCode.USER_TESTDATA_FILE_WRITE_FAILED,
    "dir_not_found_user": ResultCode.USER_TESTDATA_SAVE_FAILED,
    "invalid_uuid_user": ResultCode.USER_TESTDATA_SAVE_FAILED,
    "not_a_dict_user": ResultCode.USER_TESTDATA_SAVE_FAILED,
    "file_not_found_user": ResultCode.USER_TESTDATA_FILE_WRITE_FAILED,
    "file_empty_or_invalid_user": ResultCode.USER_TESTDATA_FILE_WRITE_FAILED,
    "missing_user_field": ResultCode.USER_UUID_ATTACH_FAILED,
    "faker_error_user": ResultCode.USER_UUID_ATTACH_FAILED,

    # 商品
    "save_failed_product": ResultCode.PRODUCT_TESTDATA_SAVE_FAILED,
    "dir_not_found_product": ResultCode.PRODUCT_TESTDATA_SAVE_FAILED,
    "missing_product_field": ResultCode.PRODUCT_UUID_ATTACH_FAILED,
    "faker_error_product": ResultCode.PRODUCT_UUID_ATTACH_FAILED,
    "empty_categories": ResultCode.PRODUCT_GENERATION_FAILED,
    "unexpected_exception": ResultCode.PRODUCT_GENERATION_FAILED,

    # file_helper, data_loader
    "file_not_found": ResultCode.FILE_NOT_FOUND,
    "load_json_failed": ResultCode.FILE_LOAD_FAILED,
    "save_failed": ResultCode.FILE_WRITE_FAILED,
    "save_returned_false": ResultCode.UNKNOWN_FILE_SAVE_ERROR,
    "permission_denied": ResultCode.FILE_PERMISSION_DENIED,
    "encoding_error": ResultCode.FILE_ENCODING_ERROR,
    "path_generation_failed": ResultCode.FILE_PATH_GENERATION_FAILED,
    "json_serialization_failed": ResultCode.FILE_SERIALIZATION_FAILED,
    "file_empty_or_invalid": ResultCode.INVALID_FILE_DATA,

    # 資料驗證類
    "invalid_uuid": ResultCode.UUID_FORMAT_INVALID,
    "invalid_kind": ResultCode.INVALID_FILE_KIND,
    "not_a_dict": ResultCode.INVALID_DATA_TYPE,
    "enrich_failed": ResultCode.ENRICH_UUID_FAILED,

    # uuid
    "uuid_generate_failed": ResultCode.UUID_GEN_FAIL,
}


# 錯誤碼對應訊息表（供 log_helper 使用）
ERROR_CODE_MSG_MAP = {
    ResultCode.SUCCESS: "success",
    ResultCode.USER_TESTDATA_SAVE_FAILED: "無法儲存使用者測資",
    ResultCode.USER_TESTDATA_ALREADY_EXISTS: "使用者測資已存在",
    ResultCode.USER_TESTDATA_FILE_WRITE_FAILED: "寫入使用者測資失敗",
    ResultCode.USER_UUID_ATTACH_FAILED: "附加使用者 UUID 失敗",
    ResultCode.PRODUCT_TESTDATA_SAVE_FAILED: "無法儲存商品測資",
    ResultCode.PRODUCT_TESTDATA_ALREADY_EXISTS: "商品測資已存在",
    ResultCode.PRODUCT_TESTDATA_FILE_WRITE_FAILED: "寫入商品測資失敗",
    ResultCode.PRODUCT_UUID_ATTACH_FAILED: "附加商品 UUID 失敗",
    ResultCode.TESTDATA_DIR_PREPARE_FAILED: "建立測資資料夾失敗",
    ResultCode.TESTDATA_GENERATION_SUCCESS: "測資產生任務完成",
    ResultCode.UUID_GEN_FAIL: "UUID 產生失敗",
    ResultCode.FILE_NOT_FOUND: "找不到檔案",
    ResultCode.FILE_LOAD_FAILED: "讀取檔案失敗",
    ResultCode.FILE_WRITE_FAILED: "寫入檔案失敗",
    ResultCode.FILE_PERMISSION_DENIED: "檔案存取權限不足",
    ResultCode.FILE_ENCODING_ERROR: "檔案編碼錯誤",
    ResultCode.FILE_PATH_GENERATION_FAILED: "產生儲存路徑失敗",
    ResultCode.FILE_SERIALIZATION_FAILED: "JSON 序列化失敗",
    ResultCode.INVALID_FILE_DATA: "檔案為空或資料不合法",
    ResultCode.UNKNOWN_FILE_SAVE_ERROR: "檔案儲存時發生未知錯誤",

    ResultCode.UUID_FORMAT_INVALID: "UUID 格式不正確",
    ResultCode.INVALID_FILE_KIND: "資料類型錯誤",
    ResultCode.INVALID_DATA_TYPE: "傳入資料不是 dict",
    ResultCode.ENRICH_UUID_FAILED: "UUID 注入失敗",
    
}
