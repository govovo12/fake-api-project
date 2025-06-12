class ResultCode:
    """
    定義系統中所有標準錯誤碼與成功碼
    """

    # ✅ 成功區（供 log_step 使用）
    SUCCESS = 0  # 成功回報
    SUCCESS_CODES = {
        SUCCESS: "操作成功",
    }

    # ✅ 工具區錯誤碼（file_helper、data_loader、uuid_generator 等）
    TOOL_FILE_WRITE_FAILED = 40010
    TOOL_UUID_GEN_FAILED = 40011
    TOOL_DIR_CREATE_FAILED = 40012
    TOOL_FILE_CREATE_FAILED = 40013
    TOOL_FILE_STAT_FAILED = 40014
    TOOL_FILE_CLEAR_FAILED = 40015
    TOOL_FILE_PERMISSION_DENIED = 40017
    TOOL_FILE_LOAD_FAILED = 40018
    TOOL_INVALID_FILE_KIND = 40019
    TOOL_INVALID_FILE_DATA = 40020
    TOOL_TEMP_FILE_WRITE_FAILED = 40021

    # ✅ 新增的錯誤碼（以 TOOL_ 開頭）
    TOOL_USER_TESTDATA_FILE_WRITE_FAILED = 40022  # 自定義錯誤碼，測試資料檔案寫入失敗

    # ✅ 任務模組錯誤碼（user_generator, product_generator）
    PRODUCT_CATEGORY_EMPTY = 41001  # 商品類別為空
    PRODUCT_GENERATION_FAILED = 41002  # 商品生成失敗
    FAKER_GENERATE_FAILED = 42001  # 用戶資料生成失敗

    # ✅ 通用錯誤碼
    UUID_GEN_FAIL = 42003
    TOOL_FILE_NOT_FOUND = 42002

    # ✅ 錯誤訊息對應表
    ERROR_MESSAGES = {
        TOOL_FILE_WRITE_FAILED: "檔案寫入失敗",
        TOOL_UUID_GEN_FAILED: "UUID 生成失敗",
        TOOL_DIR_CREATE_FAILED: "目錄創建失敗",
        TOOL_FILE_CREATE_FAILED: "檔案創建失敗",
        TOOL_FILE_STAT_FAILED: "檔案狀態檢查失敗",
        TOOL_FILE_CLEAR_FAILED: "檔案清空失敗",
        TOOL_FILE_PERMISSION_DENIED: "檔案權限不足",
        TOOL_FILE_LOAD_FAILED: "檔案載入失敗",
        TOOL_INVALID_FILE_KIND: "錯誤的檔案類型",
        TOOL_INVALID_FILE_DATA: "檔案資料格式錯誤",
        TOOL_TEMP_FILE_WRITE_FAILED: "暫存檔寫入失敗",
        UUID_GEN_FAIL: "UUID 生成失敗",
        TOOL_FILE_NOT_FOUND: "檔案未找到",
        TOOL_USER_TESTDATA_FILE_WRITE_FAILED: "測試資料檔案寫入失敗",  # 自定義錯誤碼的訊息
        PRODUCT_CATEGORY_EMPTY: "商品類別為空",
        PRODUCT_GENERATION_FAILED: "商品生成失敗",
        FAKER_GENERATE_FAILED: "用戶資料生成失敗",
    }
