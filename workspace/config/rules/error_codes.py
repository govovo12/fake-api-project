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
    }
