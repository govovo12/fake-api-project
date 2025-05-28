import pytest
from workspace.utils.asserts import assert_helper

@pytest.mark.asserts
def test_assert_status_code_pass():
    class Response: status_code = 200
    assert_helper.assert_status_code(Response(), 200)

@pytest.mark.asserts
def test_assert_status_code_fail():
    class Response: status_code = 404
    with pytest.raises(AssertionError) as exc:
        assert_helper.assert_status_code(Response(), 200)
    assert "Expected status code 200, got 404" in str(exc.value)

@pytest.mark.asserts
def test_assert_in_keys_pass():
    obj = {"id": 1, "name": "John"}
    assert_helper.assert_in_keys(obj, ["id", "name"])

@pytest.mark.asserts
def test_assert_in_keys_fail():
    obj = {"id": 1}
    with pytest.raises(AssertionError) as exc:
        assert_helper.assert_in_keys(obj, ["id", "name"])
    assert "Missing keys in response" in str(exc.value)

@pytest.mark.asserts
def test_assert_json_equal_pass():
    actual = {"b": 2, "a": 1}
    expected = {"a": 1, "b": 2}
    assert_helper.assert_json_equal(actual, expected)

@pytest.mark.asserts
def test_assert_json_equal_fail():
    actual = {"a": 1, "b": 3}
    expected = {"a": 1, "b": 2}
    with pytest.raises(AssertionError):
        assert_helper.assert_json_equal(actual, expected)

@pytest.mark.asserts
def test_assert_contains_substring_pass():
    assert_helper.assert_contains_substring("hello world", "world")

@pytest.mark.asserts
def test_assert_contains_substring_fail():
    with pytest.raises(AssertionError):
        assert_helper.assert_contains_substring("hello world", "foo")
