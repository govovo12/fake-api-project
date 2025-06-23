class ResultCode:
    """
    系統統一回傳碼定義（成功碼 / 各任務錯誤碼 / 工具錯誤碼）
    """

    # ------------------------
    # ✅ 成功碼（0～10xxx）
    # ------------------------
    SUCCESS = 0  # 通用成功
    TESTDATA_TASK_SUCCESS = 10000
    REGISTER_TASK_SUCCESS = 10001
    LOGIN_TASK_SUCCESS = 10002
    CREATE_PRODUCT_SUCCESS = 10003
    CREATE_CART_SUCCESS = 10004
    TASK_CLEAN_TESTDATA_SUCCESS = 10005
    MASTER_TASK_SUCCESS = 90000  # 主控流程成功完成
    # ------------------------
    # ❌ 通用錯誤（6xxx）
    # ------------------------
    REQUESTS_EXCEPTION = 6000
    SERVER_ERROR = 6001

    # ------------------------
    # ❌ 工具模組錯誤碼（40010～）
    # ------------------------
    TOOL_DIR_CREATE_FAILED = 40010
    TOOL_FILE_CLEAR_FAILED = 40011
    TOOL_FILE_CREATE_FAILED = 40012
    TOOL_FILE_LOAD_FAILED = 40013
    TOOL_FILE_PERMISSION_DENIED = 40014
    TOOL_FILE_STAT_FAILED = 40015
    TOOL_FILE_WRITE_FAILED = 40016
    TOOL_INVALID_FILE_DATA = 40017
    TOOL_USER_TESTDATA_FILE_WRITE_FAILED = 40018
    UUID_GEN_FAIL = 40019
    TOOL_FILE_DELETE_FAILED = 40020

    TOOL_RESPONSE_JSON_PARSE_FAILED = 40030
    TOOL_RESPONSE_DATA_MISSING = 40031
    TOOL_RESPONSE_FIELD_MISSING = 40032

    # ------------------------
    # ❌ 測資任務錯誤碼（410xx）
    # ------------------------
    PRODUCT_CATEGORY_EMPTY = 41001
    PRODUCT_GENERATION_FAILED = 41002
    CART_GENERATION_FAILED = 41003
    CREATE_PRODUCT_FAILED = 41021
    CART_CREATE_FAILED = 41022

    # ------------------------
    # ❌ 測資清除錯誤碼（4101x）
    # ------------------------
    REMOVE_USER_DATA_FAILED = 41011
    REMOVE_PRODUCT_DATA_FAILED = 41012
    REMOVE_CART_DATA_FAILED = 41013

    # ------------------------
    # ❌ 註冊任務錯誤碼（42xxx）
    # ------------------------
    FAKER_GENERATE_FAILED = 42001
    FAKER_REGISTER_FAILED = 42002
    FAKER_REGISTER_EXCEPTION = 42003

    # ------------------------
    # ❌ 登入任務錯誤碼（43xxx）
    # ------------------------
    LOGIN_API_FAILED = 43001
    LOGIN_EXCEPTION = 43002

    # ------------------------
    # ❌ 通用 fallback
    # ------------------------
    GENERIC_ERROR = 9999


def is_success(code: int) -> bool:
    return code == ResultCode.SUCCESS


ERROR_MESSAGES = {
    # ✅ 成功提示
    ResultCode.SUCCESS: "操作成功",
    ResultCode.TESTDATA_TASK_SUCCESS: "測資流程成功",
    ResultCode.REGISTER_TASK_SUCCESS: "帳號註冊成功",
    ResultCode.LOGIN_TASK_SUCCESS: "登入流程成功",
    ResultCode.CREATE_PRODUCT_SUCCESS: "商品建構成功",
    ResultCode.CREATE_CART_SUCCESS: "購物車建立成功",
    ResultCode.TASK_CLEAN_TESTDATA_SUCCESS: "測資已清除",
    ResultCode.MASTER_TASK_SUCCESS:"所有任務成功",

    # ❌ 通用
    ResultCode.REQUESTS_EXCEPTION: "連線失敗或逾時",
    ResultCode.SERVER_ERROR: "伺服器錯誤 (5xx)",

    # ❌ 工具錯誤
    ResultCode.TOOL_DIR_CREATE_FAILED: "建立目錄失敗",
    ResultCode.TOOL_FILE_CLEAR_FAILED: "清除檔案失敗",
    ResultCode.TOOL_FILE_CREATE_FAILED: "建立檔案失敗",
    ResultCode.TOOL_FILE_LOAD_FAILED: "讀取檔案失敗",
    ResultCode.TOOL_FILE_PERMISSION_DENIED: "檔案權限不足",
    ResultCode.TOOL_FILE_STAT_FAILED: "檢查檔案狀態失敗",
    ResultCode.TOOL_FILE_WRITE_FAILED: "寫入檔案失敗",
    ResultCode.TOOL_INVALID_FILE_DATA: "檔案資料格式錯誤",
    ResultCode.TOOL_USER_TESTDATA_FILE_WRITE_FAILED: "寫入使用者測資失敗",
    ResultCode.UUID_GEN_FAIL: "UUID 產生失敗",
    ResultCode.TOOL_FILE_DELETE_FAILED: "刪除檔案失敗",
    ResultCode.TOOL_RESPONSE_JSON_PARSE_FAILED: "JSON 解析錯誤",
    ResultCode.TOOL_RESPONSE_DATA_MISSING: "回傳缺少 data 欄位",
    ResultCode.TOOL_RESPONSE_FIELD_MISSING: "回傳缺少必要欄位",

    # ❌ 測資任務
    ResultCode.PRODUCT_CATEGORY_EMPTY: "商品分類為空",
    ResultCode.PRODUCT_GENERATION_FAILED: "商品產生失敗",
    ResultCode.CART_GENERATION_FAILED: "購物車資料產生失敗",
    ResultCode.CREATE_PRODUCT_FAILED: "商品建立失敗",
    ResultCode.CART_CREATE_FAILED: "購物車建立失敗",

    # ❌ 測資清除
    ResultCode.REMOVE_USER_DATA_FAILED: "刪除使用者資料失敗",
    ResultCode.REMOVE_PRODUCT_DATA_FAILED: "刪除商品資料失敗",
    ResultCode.REMOVE_CART_DATA_FAILED: "刪除購物車資料失敗",

    # ❌ 註冊登入
    ResultCode.FAKER_GENERATE_FAILED: "帳號產生失敗",
    ResultCode.FAKER_REGISTER_FAILED: "註冊 API 呼叫失敗",
    ResultCode.FAKER_REGISTER_EXCEPTION: "註冊流程發生例外",
    ResultCode.LOGIN_API_FAILED: "登入 API 呼叫失敗",
    ResultCode.LOGIN_EXCEPTION: "登入流程發生例外",

    # fallback
    ResultCode.GENERIC_ERROR: "未知錯誤",
}


# ------------------------
# ✅ 錯誤碼分類（供 log 工具使用）
# ------------------------

SUCCESS_CODES = {
    ResultCode.SUCCESS,
    ResultCode.TESTDATA_TASK_SUCCESS,
    ResultCode.REGISTER_TASK_SUCCESS,
    ResultCode.LOGIN_TASK_SUCCESS,
    ResultCode.CREATE_PRODUCT_SUCCESS,
    ResultCode.CREATE_CART_SUCCESS,
    ResultCode.TASK_CLEAN_TESTDATA_SUCCESS,
    ResultCode.MASTER_TASK_SUCCESS,
}

TOOL_ERROR_CODES = {
    ResultCode.REQUESTS_EXCEPTION,
    ResultCode.SERVER_ERROR,
    ResultCode.TOOL_DIR_CREATE_FAILED,
    ResultCode.TOOL_FILE_CLEAR_FAILED,
    ResultCode.TOOL_FILE_CREATE_FAILED,
    ResultCode.TOOL_FILE_LOAD_FAILED,
    ResultCode.TOOL_FILE_PERMISSION_DENIED,
    ResultCode.TOOL_FILE_STAT_FAILED,
    ResultCode.TOOL_FILE_WRITE_FAILED,
    ResultCode.TOOL_INVALID_FILE_DATA,
    ResultCode.TOOL_USER_TESTDATA_FILE_WRITE_FAILED,
    ResultCode.TOOL_FILE_DELETE_FAILED,
    ResultCode.TOOL_RESPONSE_JSON_PARSE_FAILED,
    ResultCode.TOOL_RESPONSE_DATA_MISSING,
    ResultCode.TOOL_RESPONSE_FIELD_MISSING,
    ResultCode.UUID_GEN_FAIL,
}

TASK_ERROR_CODES = {
    ResultCode.PRODUCT_CATEGORY_EMPTY,
    ResultCode.PRODUCT_GENERATION_FAILED,
    ResultCode.CART_GENERATION_FAILED,
    ResultCode.CREATE_PRODUCT_FAILED,
    ResultCode.CART_CREATE_FAILED,
    ResultCode.REMOVE_USER_DATA_FAILED,
    ResultCode.REMOVE_PRODUCT_DATA_FAILED,
    ResultCode.REMOVE_CART_DATA_FAILED,
    ResultCode.FAKER_GENERATE_FAILED,
    ResultCode.FAKER_REGISTER_FAILED,
    ResultCode.FAKER_REGISTER_EXCEPTION,
    ResultCode.LOGIN_API_FAILED,
    ResultCode.LOGIN_EXCEPTION,
}

GENERIC_ERROR_CODES = {
    ResultCode.GENERIC_ERROR,
}
