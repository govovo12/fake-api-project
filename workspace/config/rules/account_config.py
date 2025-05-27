from dotenv import load_dotenv
from config.paths import ACCOUNT_ENV_PATH
import os

# 正確載入 .env 檔案
load_dotenv(dotenv_path=ACCOUNT_ENV_PATH)

# Debug 用：確認有成功讀到環境變數
print("USERNAME_PREFIX:", os.getenv("USERNAME_PREFIX"))
print("USERNAME_LENGTH:", os.getenv("USERNAME_LENGTH"))
print("PASSWORD_LENGTH:", os.getenv("PASSWORD_LENGTH"))
print("ACCOUNT_GEN_COUNT:", os.getenv("ACCOUNT_GEN_COUNT"))

# 將環境變數轉換成實際型別與變數
USERNAME_PREFIX = os.getenv("USERNAME_PREFIX")
USERNAME_LENGTH = int(os.getenv("USERNAME_LENGTH"))
PASSWORD_LENGTH = int(os.getenv("PASSWORD_LENGTH"))
ACCOUNT_GEN_COUNT = int(os.getenv("ACCOUNT_GEN_COUNT"))

# 原始變數保留（可獨立使用）
ACCOUNT_GEN_USERNAME_PREFIX = USERNAME_PREFIX
ACCOUNT_GEN_USERNAME_LENGTH = USERNAME_LENGTH
ACCOUNT_GEN_PASSWORD_LENGTH = PASSWORD_LENGTH
ACCOUNT_GEN_COUNT = ACCOUNT_GEN_COUNT

# 主設定物件，提供給 controller 使用
ACCOUNT_GEN_CONFIG = {
    "rules": {
        "username": {
            "prefix": USERNAME_PREFIX,
            "length": USERNAME_LENGTH
        },
        "password": {
            "length": PASSWORD_LENGTH
        }
    },
    "params": {
        "generate_count": ACCOUNT_GEN_COUNT
    }
}
