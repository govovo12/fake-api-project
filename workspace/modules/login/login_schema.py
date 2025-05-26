from dataclasses import dataclass
from typing import Optional

@dataclass
class LoginRequest:
    username: str
    password: str
    timeout: int = 10

@dataclass
class LoginResult:
    success: bool
    token: Optional[str] = None
    error_code: Optional[int] = None
    error_msg: Optional[str] = None
    status_code: Optional[int] = None