# workspace/config/rules/error_codes.py
# 用於集中定義所有模組的數值型錯誤碼與對應訊息
# 錯誤碼為 int，可用於 log、報告、通知等

# === 錯誤碼定義（常數） ===
ACCOUNT_GEN_FAIL = 1001
ACCOUNT_SAVE_FAIL = 1002

LOGIN_API_FAIL = 2001
LOGIN_RESPONSE_INVALID = 2002
LOGIN_CREDENTIAL_FAIL = 2003

API_TIMEOUT = 9001
API_RESPONSE_FORMAT_ERROR = 9002

# === 錯誤碼對應說明（字典） ===
ERROR_MESSAGES = {
    ACCOUNT_GEN_FAIL: "帳號產生器發生錯誤，請檢查輸入參數或隨機工具是否可用",
    ACCOUNT_SAVE_FAIL: "帳號寫入檔案失敗，請確認路徑與寫入權限",

    LOGIN_API_FAIL: "登入 API 請求失敗，可能為連線中斷或超時",
    LOGIN_RESPONSE_INVALID: "登入回傳格式錯誤，找不到 token 或回應無法解析",
    LOGIN_CREDENTIAL_FAIL: "登入失敗，帳號或密碼錯誤",

    API_TIMEOUT: "API 請求逾時或無回應",
    API_RESPONSE_FORMAT_ERROR: "API 回應格式無法解析或遺漏必要欄位"
}
