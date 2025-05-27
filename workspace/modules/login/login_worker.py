import os
import requests
from dotenv import load_dotenv
from config.paths import LOGIN_ENV_PATH
from .login_schema import LoginRequest, LoginResult
from config.rules import error_codes
from config.rules.login_config import LOGIN_HEADERS, LOGIN_TIMEOUT

# ✅ 統一從 LOGIN_ENV_PATH 載入 .env 檔案
load_dotenv(dotenv_path=LOGIN_ENV_PATH)


def do_login(req: LoginRequest) -> LoginResult:
    url = os.getenv("LOGIN_API_URL", "https://fakestoreapi.com/auth/login")
    headers = LOGIN_HEADERS
    payload = {"username": req.username, "password": req.password}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=req.timeout or LOGIN_TIMEOUT)
    except requests.RequestException:
        return LoginResult(
            success=False,
            error_code=error_codes.LOGIN_API_FAIL,
            status_code=None
        )

    if response.status_code == 200:
        try:
            data = response.json()
            token = data.get("token")
            if token:
                return LoginResult(success=True, token=token, status_code=200)
            else:
                return LoginResult(
                    success=False,
                    error_code=error_codes.LOGIN_RESPONSE_INVALID,
                    status_code=200
                )
        except Exception:
            return LoginResult(
                success=False,
                error_code=error_codes.LOGIN_RESPONSE_INVALID,
                status_code=200
            )
    elif response.status_code == 401:
        return LoginResult(
            success=False,
            error_code=error_codes.LOGIN_CREDENTIAL_FAIL,
            status_code=401
        )
    else:
        return LoginResult(
            success=False,
            error_code=error_codes.LOGIN_API_FAIL,
            status_code=response.status_code
        )
