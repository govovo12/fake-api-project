class ResultCode:
    # ✅【通用】
    SUCCESS = 0                          # 成功

    # 🧪【測資生產器】
    UUID_GEN_FAIL = 10101               # UUID 產生失敗（已實作，用於假資料生成）
    ACCOUNT_GEN_FAIL = 20101            # 假帳號產生失敗（測資用）
    USER_WRITE_FAIL = 20201             # 寫入用戶資料失敗（測資寫檔）

    PRODUCT_GEN_FAIL = 30101            # 假商品產生失敗（測資用）
    PRODUCT_WRITE_FAIL = 30201          # 寫入商品資料失敗（測資寫檔）

    # ✅【註冊流程任務模組：有實作】
    REGISTER_API_FAIL = 40101           # ✅ 註冊 API 回傳錯誤（有用）
    REGISTER_API_EXCEPTION = 40102      # ❌ 未實作（預留給 try/except 錯誤處理）
    TOKEN_EXTRACTION_FAIL = 40103       # ❌ 未實作（假設未來登入用）
    SAVE_ENV_FAIL = 40104               # ❌ 未實作（預留未來登入成功後寫入）

    USER_TESTDATA_NOT_FOUND = 40105     # ✅ 找不到 user 測試資料（有用）
    PAYLOAD_BUILD_FAIL = 40106          # ✅ 註冊 payload 組裝失敗（有用）

    # 🔁【預留給 retry / 超時】
    API_TIMEOUT = 90001                 # ❌ 未實作（預留 timeout）


# ✅ 錯誤碼對應說明表，供 log_helper 等模組引用
ERROR_CODE_MSG_MAP = {
    0: "成功",

    # 🧪 測資生成器
    10101: "UUID 產生失敗",
    20101: "假帳號產生失敗",
    20201: "寫入用戶資料失敗",
    30101: "假商品產生失敗",
    30201: "寫入商品資料失敗",

    # ✅ 任務流程錯誤碼（有實作）
    40101: "註冊 API 回傳錯誤",
    40105: "找不到 user 測試資料",
    40106: "註冊 payload 組裝失敗",

    # ❌ 尚未實作（預留）
    40102: "註冊 API 發生例外",
    40103: "Token 擷取失敗",
    40104: "儲存登入憑證失敗",
    90001: "API 請求逾時"
}
