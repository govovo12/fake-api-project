import pytest
from workspace.utils.retry.retry_handler import retry_on_code

pytestmark = [pytest.mark.unit, pytest.mark.retry]


def test_retry_success_first_try():
    """✅ 測試第一次成功不進入 retry（回傳 tuple）"""
    def mock_func():
        return 10002, "token123"

    wrapped = retry_on_code(mock_func, retry_codes=[43002])
    result = wrapped()

    assert isinstance(result, tuple)
    assert result == (10002, "token123")


def test_retry_all_fail():
    """❌ 測試每次都回傳錯誤碼 → 最後一次失敗（回傳 tuple）"""
    calls = []

    def mock_func():
        calls.append(1)
        return 43002, None

    wrapped = retry_on_code(mock_func, retry_codes=[43002], max_retries=3)
    result = wrapped()

    assert result == (43002, None)
    assert len(calls) == 3


def test_retry_then_success():
    """⚠️ 第一次失敗、第二次成功，應停止 retry（回傳 tuple）"""
    calls = []

    def mock_func():
        calls.append(1)
        if len(calls) == 1:
            return 43002, None
        return 10002, "tokenOK"

    wrapped = retry_on_code(mock_func, retry_codes=[43002], max_retries=3)
    result = wrapped()

    assert result == (10002, "tokenOK")
    assert len(calls) == 2


def test_retry_non_retryable_code():
    """測試回傳非 retry code 應直接返回（回傳 tuple）"""
    def mock_func():
        return 43001, None

    wrapped = retry_on_code(mock_func, retry_codes=[43002])
    result = wrapped()

    assert result == (43001, None)


def test_retry_with_int_only():
    """✅ 測試任務回傳單一錯誤碼 int，也能正確 retry 並返回"""
    calls = []

    def mock_func():
        calls.append(1)
        if len(calls) < 3:
            return 43002  # 重試碼
        return 10006  # 最後成功

    wrapped = retry_on_code(mock_func, retry_codes=[43002], max_retries=5)
    result = wrapped()

    assert result == 10006
    assert len(calls) == 3


def test_retry_int_all_fail():
    """❌ 測試只回 int，且全部失敗"""
    calls = []

    def mock_func():
        calls.append(1)
        return 43002  # 都是重試碼

    wrapped = retry_on_code(mock_func, retry_codes=[43002], max_retries=4)
    result = wrapped()

    assert result == 43002
    assert len(calls) == 4
