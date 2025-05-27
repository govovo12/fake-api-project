import json
from typing import List
from pathlib import Path
from .login_schema import LoginRequest
from config.paths import ACCOUNT_GEN_DATA_JSON


def read_login_requests(json_path: Path = ACCOUNT_GEN_DATA_JSON) -> List[LoginRequest]:
    """
    從指定 JSON 讀取 login 測資，產生 LoginRequest 清單
    JSON 格式需為：
    {
        "accounts": [
            {"username": "abc", "password": "123"},
            ...
        ]
    }
    """
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    accounts = data if isinstance(data, list) else data.get("accounts", [])
    return [LoginRequest(username=a["username"], password=a["password"]) for a in accounts if "username" in a and "password" in a]
