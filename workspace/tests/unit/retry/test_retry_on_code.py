import pytest
from workspace.utils.retry.retry_handler import retry_on_code

pytestmark = [pytest.mark.unit, pytest.mark.retry]


def test_retry_success_first_try():
    """✅ 測試第一次成功不進入 retry"""
    def mock_func():
        return 10002, "token123"  # 成功碼

    wrapped = retry_on_code(mock_func, retry_codes=[43002])
    code, payload = wrapped()

    assert code == 10002
    assert payload == "token123"


def test_retry_all_fail():
    """❌ 測試每次都回傳錯誤碼 → 最後一次失敗"""
    calls = []

    def mock_func():
        calls.append(1)
        return 43002, None  # 重試碼

    wrapped = retry_on_code(mock_func, retry_codes=[43002], max_retries=3)
    code, payload = wrapped()

    assert code == 43002
    assert payload is None
    assert len(calls) == 3


def test_retry_then_success():
    """⚠️ 第一次失敗、第二次成功，應停止 retry"""
    calls = []

    def mock_func():
        calls.append(1)
        if len(calls) == 1:
            return 43002, None  # 第一次錯誤
        return 10002, "tokenOK"  # 第二次成功

    wrapped = retry_on_code(mock_func, retry_codes=[43002], max_retries=3)
    code, payload = wrapped()

    assert code == 10002
    assert payload == "tokenOK"
    assert len(calls) == 2


def test_retry_non_retryable_code():
    """測試回傳非 retry code 應直接返回"""
    def mock_func():
        return 43001, None  # 這不是可 retry 的錯誤碼

    wrapped = retry_on_code(mock_func, retry_codes=[43002])
    code, payload = wrapped()

    assert code == 43001
    assert payload is None
