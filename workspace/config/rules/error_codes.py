# config/rules/error_codes.py

class ResultCode:
    SUCCESS = 0
    UUID_GEN_FAIL = 10101
    ACCOUNT_GEN_FAIL = 20101
    USER_WRITE_FAIL = 20201
    PRODUCT_GEN_FAIL = 30101
    PRODUCT_WRITE_FAIL = 30201
    REGISTER_API_FAIL = 40101
    REGISTER_API_EXCEPTION = 40102
    TOKEN_EXTRACTION_FAIL = 40103
    SAVE_ENV_FAIL = 40104
    USER_TESTDATA_NOT_FOUND = 40105
    PAYLOAD_BUILD_FAIL = 40106
    API_TIMEOUT = 90001

# 錯誤碼對應中文說明
ERROR_CODE_MSG_MAP = {
    0: "成功",
    10101: "UUID 產生失敗",
    20101: "假帳號產生失敗",
    20201: "寫入用戶資料失敗",
    30101: "假商品產生失敗",
    30201: "寫入商品資料失敗",
    40101: "註冊 API 回傳錯誤",
    40102: "註冊 API 發生例外",
    40103: "Token 擷取失敗",
    40104: "儲存登入憑證失敗",
    40105: "找不到 user 測試資料",
    40106: "註冊 payload 組裝失敗",
    90001: "API 請求逾時"
}
