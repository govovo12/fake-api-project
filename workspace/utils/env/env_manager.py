# utils/env/env_manager.py
import os
from pathlib import Path
from dotenv import load_dotenv
from controller import log_controller

_env_loaded = False


def load_env(filename: str) -> None:
    """
    載入指定 .env 檔案（從 config/envs/ 底下），例如 "account_gen.env"
    """
    from config import paths
    global _env_loaded

    env_path = paths.ENV_PATH / filename
    if not env_path.exists():
        log_controller.warn(f"找不到 .env 檔案：{filename}")
        return

    load_dotenv(dotenv_path=env_path, override=True)
    _env_loaded = True
    log_controller.info(f"成功載入環境設定檔：{filename}")


def get_env(key: str, default: str = "") -> str:
    """
    取得環境變數，若不存在則回傳 default。
    """
    value = os.getenv(key, default)
    if not value:
        log_controller.warn(f"讀取環境變數失敗：{key}，使用預設值")
    return value
