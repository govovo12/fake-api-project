import json
from pathlib import Path
from typing import List
from .login_schema import LoginRequest


BASE_DIR = Path(__file__).resolve().parents[2]  # 回到 workspace/
DEFAULT_LOGIN_JSON = BASE_DIR / "testdata" / "login" / "valid_case.json"


def read_login_requests(json_path: Path = DEFAULT_LOGIN_JSON) -> List[LoginRequest]:
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
