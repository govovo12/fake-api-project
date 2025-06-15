class ResultCode:
    """
    定義系統中所有標準錯誤碼與成功碼
    """
   
    # ✅ 成功區錯誤碼
    SUCCESS = 0  # 通用成功
    TESTDATA_TASK_SUCCESS = 10000 # 測資任務成功完成
    REGISTER_TASK_SUCCESS = 10001  # 註冊任務成功（子控制器專用)
    LOGIN_TASK_SUCCESS = 10002  # 登入成功
    # ✅ 工具區模組錯誤碼
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
    GENERIC_ERROR = 9999  # 未知錯誤 fallback
    
    TOOL_RESPONSE_JSON_PARSE_FAILED = 40030  # response 無法解析為 JSON
    TOOL_RESPONSE_DATA_MISSING = 40031       # JSON 中無 data 區塊
    TOOL_RESPONSE_FIELD_MISSING = 40032      # 欄位不存在於 JSON 結構
    
    # ✅ 測資產生任務模組錯誤碼
    PRODUCT_CATEGORY_EMPTY = 41001  # 商品類別為空或不合法
    PRODUCT_GENERATION_FAILED = 41002  # 商品生成失敗
    FAKER_GENERATE_FAILED = 42001  # Faker 生成用戶資料失敗
    
    # 註冊任務錯誤碼 42xxx 區段
    FAKER_REGISTER_FAILED = 42002           # 註冊失敗（API 回應非 2xx）
    FAKER_REGISTER_EXCEPTION = 42003        # 註冊過程中發生 requests 例外

    # === 任務層：登入任務 ===
    LOGIN_API_FAILED = 43001    # 登入 API 回傳非 200（如 401 Unauthorized）
    LOGIN_EXCEPTION = 43002     # 登入時發生 requests 例外（timeout、連線失敗等）

    @classmethod
    def is_success(cls, code: int) -> bool:
        return code in {
            cls.SUCCESS,
            cls.TESTDATA_TASK_SUCCESS,
            cls.REGISTER_TASK_SUCCESS,
            cls.LOGIN_TASK_SUCCESS,
    }

    # ✅ 錯誤訊息對應表
    ERROR_MESSAGES = {
        SUCCESS: "操作成功",
         TESTDATA_TASK_SUCCESS: "測資任務成功完成",
         REGISTER_TASK_SUCCESS: "註冊任務成功完成",
         LOGIN_TASK_SUCCESS: "登入任務成功完成",

        TOOL_DIR_CREATE_FAILED: "資料夾建立失敗",
        TOOL_FILE_CLEAR_FAILED: "檔案清空失敗",
        TOOL_FILE_CREATE_FAILED: "檔案建立失敗",
        TOOL_FILE_LOAD_FAILED: "檔案載入失敗",
        TOOL_FILE_PERMISSION_DENIED: "檔案權限不足",
        TOOL_FILE_STAT_FAILED: "檔案狀態檢查失敗",
        TOOL_FILE_WRITE_FAILED: "檔案寫入失敗",
        TOOL_INVALID_FILE_DATA: "檔案資料格式錯誤",
        TOOL_USER_TESTDATA_FILE_WRITE_FAILED: "測資資料檔案寫入失敗",
        UUID_GEN_FAIL: "UUID 生成失敗",

        PRODUCT_CATEGORY_EMPTY: "商品類別為空或不合法",
        PRODUCT_GENERATION_FAILED: "商品資料生成失敗",
        FAKER_GENERATE_FAILED: "用戶測資生成失敗",
        
        GENERIC_ERROR: "未知錯誤",

        TOOL_RESPONSE_JSON_PARSE_FAILED: "response 無法解析為 JSON",
        TOOL_RESPONSE_DATA_MISSING: "回傳資料缺少 data 區塊",
        TOOL_RESPONSE_FIELD_MISSING: "回傳資料中缺少指定欄位",

        FAKER_REGISTER_FAILED: "使用者註冊失敗，API 回應非預期成功碼",
        FAKER_REGISTER_EXCEPTION: "使用者註冊過程中發生連線異常或請求錯誤",

        LOGIN_API_FAILED: "登入失敗，帳號或密碼錯誤",  
        LOGIN_EXCEPTION: "登入過程發生例外，請稍後再試",  

    }

