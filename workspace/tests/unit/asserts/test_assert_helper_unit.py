import pytest
from utils.asserts import assert_helper

pytestmark = [pytest.mark.unit, pytest.mark.asserts]

def test_assert_status_code_pass():
    """status code 符合，應通過"""
    class Response: status_code = 200
    assert_helper.assert_status_code(Response(), 200)

def test_assert_status_code_fail():
    """status code 不符，應拋 AssertionError 且訊息正確"""
    class Response: status_code = 404
    with pytest.raises(AssertionError) as exc:
        assert_helper.assert_status_code(Response(), 200)
    assert "Expected status code 200, got 404" in str(exc.value)

def test_assert_in_keys_pass():
    """dict 完全包含 keys 應通過"""
    obj = {"id": 1, "name": "John"}
    assert_helper.assert_in_keys(obj, ["id", "name"])

def test_assert_in_keys_fail():
    """dict 缺 key 應拋 AssertionError 且訊息正確"""
    obj = {"id": 1}
    with pytest.raises(AssertionError) as exc:
        assert_helper.assert_in_keys(obj, ["id", "name"])
    assert "Missing keys in response" in str(exc.value)

def test_assert_json_equal_pass():
    """JSON 結構相等應通過（順序不影響）"""
    actual = {"b": 2, "a": 1}
    expected = {"a": 1, "b": 2}
    assert_helper.assert_json_equal(actual, expected)

def test_assert_json_equal_fail():
    """JSON 結構不同應拋 AssertionError 且訊息內有 JSON"""
    actual = {"a": 1, "b": 3}
    expected = {"a": 1, "b": 2}
    with pytest.raises(AssertionError) as exc:
        assert_helper.assert_json_equal(actual, expected)
    assert "JSON not equal!" in str(exc.value) or "JSON structures do not match." in str(exc.value)

def test_assert_contains_substring_pass():
    """子字串包含應通過"""
    assert_helper.assert_contains_substring("hello world", "world")

def test_assert_contains_substring_fail():
    """未包含子字串應拋 AssertionError 且訊息正確"""
    with pytest.raises(AssertionError) as exc:
        assert_helper.assert_contains_substring("hello world", "foo")
    assert "'foo' not found" in str(exc.value)
