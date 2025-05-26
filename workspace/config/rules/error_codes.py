# workspace/config/rules/error_codes.py
# 用於集中定義所有模組的數值型錯誤碼與對應訊息
# 錯誤碼為 int，可用於 log、報告、通知等

# === 錯誤碼定義（常數） ===
ACCOUNT_GEN_FAIL = 1001
ACCOUNT_SAVE_FAIL = 1002

# === 錯誤碼對應說明（字典） ===
ERROR_MESSAGES = {
    ACCOUNT_GEN_FAIL: "帳號產生器發生錯誤，請檢查輸入參數或隨機工具是否可用",
    ACCOUNT_SAVE_FAIL: "帳號寫入檔案失敗，請確認路徑與寫入權限"
}
