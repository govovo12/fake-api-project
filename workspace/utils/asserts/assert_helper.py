# ✅ 錯誤碼
from workspace.config.rules.error_codes import ResultCode


def assert_status_code(expected: int, actual: int) -> int:
    """
    驗證狀態碼是否符合預期。
    """
    if not isinstance(expected, int) or not isinstance(actual, int):
        return ResultCode.ASSERT_STATUS_CODE_MISMATCH
    return ResultCode.SUCCESS if expected == actual else ResultCode.ASSERT_STATUS_CODE_MISMATCH


def assert_keys_exist(json_data: dict, keys: list) -> int:
    """
    驗證指定鍵是否存在於 JSON 資料中。
    """
    if not isinstance(json_data, dict) or not isinstance(keys, list):
        return ResultCode.ASSERT_KEYS_MISSING
    missing_keys = [key for key in keys if key not in json_data]
    return ResultCode.SUCCESS if not missing_keys else ResultCode.ASSERT_KEYS_MISSING


def assert_json_equal(expected: dict, actual: dict) -> int:
    """
    驗證兩個 JSON 是否相等。
    """
    if not isinstance(expected, dict) or not isinstance(actual, dict):
        return ResultCode.ASSERT_JSON_MISMATCH
    return ResultCode.SUCCESS if expected == actual else ResultCode.ASSERT_JSON_MISMATCH


def assert_substring(text: str, substring: str) -> int:
    """
    驗證文字是否包含指定子字串。
    """
    if not isinstance(text, str) or not isinstance(substring, str):
        return ResultCode.ASSERT_SUBSTRING_NOT_FOUND
    return ResultCode.SUCCESS if substring in text else ResultCode.ASSERT_SUBSTRING_NOT_FOUND
