import sys
from pathlib import Path

# ➤ 設定匯入基底路徑
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# ➤ 匯入 .env 工具與主控邏輯
from workspace.utils.env.env_manager import load_env, get_env
from workspace.controller.master_controller import run
from workspace.config.paths import get_register_url, get_headers

if __name__ == "__main__":
    # ✅ 載入 .env 檔案
    env_path = BASE_DIR / ".env"
    if not load_env(env_path):
        raise FileNotFoundError("❌ 找不到 .env 檔案，請確認檔案是否存在於專案根目錄")

    # ✅ 取得 headers 與註冊 URL
    headers = get_headers()
    url = get_register_url()

    if not headers:
        raise ValueError("❌ [錯誤] 無法從 .env 解析出合法的 headers")
    if not url:
        raise ValueError("❌ [錯誤] 無法組合出註冊 API URL")

    # ✅ 取得登入帳密
    login_username = get_env("FAKESTORE_LOGIN_USERNAME")
    login_password = get_env("FAKESTORE_LOGIN_PASSWORD")

    if not login_username or not login_password:
        raise ValueError("❌ [錯誤] 請在 .env 設定 FAKESTORE_LOGIN_USERNAME 與 FAKESTORE_LOGIN_PASSWORD")

    login_cred = {
        "username": login_username,
        "password": login_password
    }

    # ✅ 呼叫主控制器
    run(headers, url, login_cred)
