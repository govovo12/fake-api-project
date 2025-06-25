import pytest

# ✅ 標記
pytestmark = [pytest.mark.unit, pytest.mark.asserts]

# ✅ 錯誤碼與斷言工具
from workspace.config.rules.error_codes import ResultCode
from workspace.utils.asserts.assert_helper import (
    assert_status_code,
    assert_keys_exist,
    assert_json_equal,
    assert_substring
)

# -------------------------
# assert_status_code 測試
# -------------------------

def test_assert_status_code_pass():
    """✅ 正向測試：預期與實際相同，應回傳 SUCCESS"""
    result = assert_status_code(200, 200)
    assert result == ResultCode.SUCCESS


def test_assert_status_code_fail():
    """❌ 反向測試：狀態碼不符，應回傳 ASSERT_STATUS_CODE_MISMATCH"""
    result = assert_status_code(200, 404)
    assert result == ResultCode.ASSERT_STATUS_CODE_MISMATCH


def test_assert_status_code_boundary():
    """⏳ 邊界測試：極端值是否相符（如 0）"""
    result = assert_status_code(0, 0)
    assert result == ResultCode.SUCCESS


def test_assert_status_code_type_error():
    """💥 錯誤模擬：傳入非 int，應判定狀態碼不相符並回傳錯誤碼"""
    result = assert_status_code("200", 200)
    assert result == ResultCode.ASSERT_STATUS_CODE_MISMATCH

# -------------------------
# assert_keys_exist 測試
# -------------------------

def test_assert_keys_exist_all_keys_present():
    """✅ 正向測試：所有 key 都存在，應回傳 SUCCESS"""
    result = assert_keys_exist({"a": 1, "b": 2}, ["a", "b"])
    assert result == ResultCode.SUCCESS


def test_assert_keys_exist_missing_keys():
    """❌ 反向測試：部分 key 缺失，應回傳 ASSERT_KEYS_MISSING"""
    result = assert_keys_exist({"a": 1}, ["a", "b"])
    assert result == ResultCode.ASSERT_KEYS_MISSING


def test_assert_keys_exist_empty_keys():
    """⏳ 邊界測試：空 key list，應視為成功"""
    result = assert_keys_exist({"a": 1}, [])
    assert result == ResultCode.SUCCESS


def test_assert_keys_exist_non_dict_input():
    """💥 錯誤模擬：傳入非 dict，應視為缺少 key 回傳錯誤碼"""
    result = assert_keys_exist("not a dict", ["a"])
    assert result == ResultCode.ASSERT_KEYS_MISSING


# -------------------------
# assert_json_equal 測試
# -------------------------

def test_assert_json_equal_exact_match():
    """✅ 正向測試：兩份 JSON 完全相同"""
    result = assert_json_equal({"a": 1}, {"a": 1})
    assert result == ResultCode.SUCCESS


def test_assert_json_equal_mismatch():
    """❌ 反向測試：兩份 JSON 不同"""
    result = assert_json_equal({"a": 1}, {"a": 2})
    assert result == ResultCode.ASSERT_JSON_MISMATCH


def test_assert_json_equal_empty_dicts():
    """⏳ 邊界測試：兩個空 dict，仍視為相同"""
    result = assert_json_equal({}, {})
    assert result == ResultCode.SUCCESS


def test_assert_json_equal_invalid_type():
    """💥 錯誤模擬：傳入非 dict，應判斷為不相等並回傳錯誤碼"""
    result = assert_json_equal(123, {"a": 1})
    assert result == ResultCode.ASSERT_JSON_MISMATCH

# -------------------------
# assert_substring 測試
# -------------------------

def test_assert_substring_found():
    """✅ 正向測試：字串包含子字串"""
    result = assert_substring("hello world", "hello")
    assert result == ResultCode.SUCCESS


def test_assert_substring_not_found():
    """❌ 反向測試：子字串不存在"""
    result = assert_substring("hello world", "bye")
    assert result == ResultCode.ASSERT_SUBSTRING_NOT_FOUND


def test_assert_substring_empty_substring():
    """⏳ 邊界測試：空子字串應總是存在"""
    result = assert_substring("anything", "")
    assert result == ResultCode.SUCCESS


def test_assert_substring_non_string_input():
    """💥 錯誤模擬：傳入非字串，應回傳 ASSERT_SUBSTRING_NOT_FOUND"""
    result = assert_substring(None, "test")
    assert result == ResultCode.ASSERT_SUBSTRING_NOT_FOUND

