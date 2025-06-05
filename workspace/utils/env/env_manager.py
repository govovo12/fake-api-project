import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values
from typing import Optional, Callable

def tool(func):
    """自製工具標記（供自動掃描工具表用）"""
    func.is_tool = True
    return func

class EnvManager:
    """
    [TOOL] 通用 .env 管理工具
    - 不綁 profile、不綁 log、不綁任何業務，只負責 load/get
    - 其他一切行為皆由呼叫方決定
    """

    def __init__(self):
        pass

    @tool
    def load_env(self, env_path: Path) -> bool:
        """
        [TOOL] 載入指定 .env 檔案，成功回傳 True，失敗 False。
        將內容寫入 os.environ
        """
        if not env_path.exists():
            return False
        load_dotenv(dotenv_path=env_path, override=True)
        return True

    @tool
    def get_env(self, key: str, default: str = "") -> str:
        """
        [TOOL] 取得環境變數，無則回傳 default。
        """
        value = os.getenv(key, default)
        return value if value is not None else default

    @staticmethod
    @tool
    def load_env_dict(env_path: Path) -> dict:
        """
        [TOOL] 讀取 .env 檔並回傳 dict（不寫入 os.environ）
        適用於資料組裝與測試用途
        """
        if not env_path.exists():
            return {}
        return dotenv_values(env_path)

# 推薦全專案共用 instance
env = EnvManager()
load_env = env.load_env
get_env = env.get_env
