# 錯誤物件
class TaskModuleError(Exception):
    def __init__(self, code: int):
        self.code = code
        super().__init__(f"[{code}]")
# ✅ 統一錯誤碼定義區
class ResultCode:
    # ✅ 成功狀態碼（供 log_helper 判斷）
    SUCCESS = 0  # 通用成功回應
    TESTDATA_GENERATION_SUCCESS = 10000  # 測資生成任務完成
    
    #測資任務工具模組+任務模組
    FILE_NOT_FOUND = 40001  # from data_loader.py
    INVALID_FILE_DATA = 40002  # from data_loader.py
    FILE_LOAD_FAILED = 40003  # from data_loader.py
    FILE_PERMISSION_DENIED = 40004  # from data_loader.py
    UNKNOWN_FILE_SAVE_ERROR = 40005  # from data_loader.py
    UUID_GEN_FAIL = 40006  # from uuid_generator.py
    USER_TESTDATA_FILE_WRITE_FAILED = 40007  # from data_initializer.py
    PRODUCT_CATEGORY_EMPTY = 40008  # from product_generator.py
    PRODUCT_GENERATION_FAILED = 40009  # from product_generator.py
    FAKER_GENERATE_FAILED = 40010  # from user_generator.py
    FILE_SERIALIZATION_FAILED = 40011  # from file_helper.py
    FILE_WRITE_FAILED = 40012  # from file_helper.py
    INVALID_FILE_KIND = 40013  # from file_helper.py
    UUID_FORMAT_INVALID = 40014  # from file_helper.py
    ENRICH_WITH_UUID_FAILED = 40024  # 資料加上 UUID 時失敗
    PRODUCT_UUID_ATTACH_FAILED = 40011  # 商品測資附加 UUID 失敗
    PRODUCT_TESTDATA_PATH_ERROR = 40012  # 商品測資路徑錯誤（UUID 或 kind 錯）
    PRODUCT_TESTDATA_SAVE_FAILED = 40013  # 商品測資儲存失敗
    TESTDATA_PRODUCT_FILE_WRITE_FAILED = 40014  # 商品測資空檔案建立失敗
    TESTDATA_USER_FILE_WRITE_FAILED = 40015  # 使用者測資空檔案建立失敗
    USER_GENERATION_FAILED = 40016  # 使用者測資資料產生失敗
    USER_UUID_ATTACH_FAILED = 40017  # 使用者資料附加 UUID 失敗
    USER_TESTDATA_ALREADY_EXISTS = 40018  # 測資 UUID 對應檔案已存在，避免覆寫
    USER_TESTDATA_SAVE_FAILED = 40019  # 使用者測資儲存失敗
    UNKNOWN_FILE_SAVE_ERROR = 40020  # 未知儲存錯誤（應為 LOAD 錯，可考慮改名）



# ✅ 錯誤訊息對應表（供 log_helper 查錯誤碼用）

ERROR_MESSAGES = {
    
    # ✅ 成功狀態碼（供 log_helper 判斷）
    ResultCode.SUCCESS: "OK",
    ResultCode.TESTDATA_GENERATION_SUCCESS: "Test data generation completed",
    #測資任務工具模組+任務模組
    ResultCode.FILE_NOT_FOUND: "找不到指定的檔案",
    ResultCode.INVALID_FILE_DATA: "檔案內容格式錯誤，應為 dict",
    ResultCode.FILE_LOAD_FAILED: "JSON 解析失敗，檔案內容非合法格式",
    ResultCode.FILE_PERMISSION_DENIED: "檔案讀取失敗，權限不足",
    ResultCode.UNKNOWN_FILE_SAVE_ERROR: "檔案載入時發生未知錯誤",
    ResultCode.UUID_GEN_FAIL: "UUID 產生失敗",
    ResultCode.USER_TESTDATA_FILE_WRITE_FAILED: "使用者測資寫入失敗",
    ResultCode.PRODUCT_CATEGORY_EMPTY: "商品分類清單為空，無法產生分類",
    ResultCode.PRODUCT_GENERATION_FAILED: "商品資料產生失敗",
    ResultCode.FAKER_GENERATE_FAILED: "使用 Faker 產生假資料時發生錯誤",
    ResultCode.FILE_SERIALIZATION_FAILED: "無法序列化資料為 JSON 格式",
    ResultCode.FILE_WRITE_FAILED: "檔案寫入失敗",
    ResultCode.INVALID_FILE_KIND: "無效的資料類型，應為 user 或 product",
    ResultCode.UUID_FORMAT_INVALID: "UUID 格式不正確，必須為 32 字元十六進位字串",
    ResultCode.ENRICH_WITH_UUID_FAILED: "將資料附加 UUID 時發生錯誤",
    ResultCode.PRODUCT_UUID_ATTACH_FAILED: "附加 UUID 至商品資料時發生錯誤",
    ResultCode.PRODUCT_TESTDATA_PATH_ERROR: "商品測資路徑錯誤，可能為 UUID 或類型無效",
    ResultCode.PRODUCT_TESTDATA_SAVE_FAILED: "商品測資寫入檔案失敗",
    ResultCode.TESTDATA_PRODUCT_FILE_WRITE_FAILED: "初始化商品測資空檔案失敗",
    ResultCode.TESTDATA_USER_FILE_WRITE_FAILED: "初始化使用者測資空檔案失敗",
    ResultCode.USER_GENERATION_FAILED: "產生使用者測資資料時發生錯誤",
    ResultCode.USER_UUID_ATTACH_FAILED: "附加 UUID 至使用者資料時發生錯誤",
    ResultCode.USER_TESTDATA_ALREADY_EXISTS: "使用者或商品測資檔案已存在，避免覆寫",
    ResultCode.USER_TESTDATA_SAVE_FAILED: "使用者測資寫入檔案失敗",
    ResultCode.UNKNOWN_FILE_SAVE_ERROR: "發生未知儲存錯誤，請確認磁碟權限或路徑正確",



}

# ✅ 成功狀態碼（供 log_helper 判斷）
SUCCESS_CODES = {
    ResultCode.SUCCESS: "通用成功",
    ResultCode.TESTDATA_GENERATION_SUCCESS: "測資任務完成",
}


