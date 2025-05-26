# workspace/config/rules/login_config.py
# login 模組用常數定義，與環境變數互補（不變的業務參數放這裡）

LOGIN_TIMEOUT = 10

LOGIN_HEADERS = {
    "Content-Type": "application/json"
}

LOGIN_RETRY_COUNT = 3
LOGIN_RETRY_DELAY = 1.0
LOGIN_RETRY_BACKOFF = 1.0
