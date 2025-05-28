import requests
from typing import Any, Dict, Optional
from controller.retry_controller import run_with_retry
from controller import log_controller

DEFAULT_TIMEOUT = 5  # seconds


def get(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = DEFAULT_TIMEOUT
) -> requests.Response:
    """
    封裝 GET 請求，內建 retry 與 log 控制。
    """
    def request():
        response = requests.get(url, headers=headers, params=params, timeout=timeout)
        _log_response("GET", url, response)
        return response

    return run_with_retry(request)


def post(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    json: Optional[Dict[str, Any]] = None,
    timeout: int = DEFAULT_TIMEOUT
) -> requests.Response:
    """
    封裝 POST 請求，內建 retry 與 log 控制。
    """
    def request():
        response = requests.post(url, headers=headers, json=json, timeout=timeout)
        _log_response("POST", url, response)
        return response

    return run_with_retry(request)


def _log_response(method: str, url: str, response: requests.Response):
    """
    通用回應紀錄函式。
    """
    if response.ok:
        log_controller.info(f"[{method}] {url} → {response.status_code}")
    else:
        log_controller.error(f"[{method}] {url} → {response.status_code}", code="API_FAIL")
