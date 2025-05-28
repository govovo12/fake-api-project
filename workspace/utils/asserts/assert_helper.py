import json


def assert_status_code(response, expected: int):
    actual = response.status_code
    assert actual == expected, f"Expected status code {expected}, got {actual}"


def assert_in_keys(obj: dict, keys: list):
    missing = [key for key in keys if key not in obj]
    assert not missing, f"Missing keys in response: {missing}"


def assert_json_equal(actual_json: dict, expected_json: dict):
    actual_str = json.dumps(actual_json, sort_keys=True)
    expected_str = json.dumps(expected_json, sort_keys=True)
    assert actual_str == expected_str, "JSON structures do not match.\nActual: {actual_str}\nExpected: {expected_str}"


def assert_contains_substring(text: str, substring: str):
    assert substring in text, f"'{substring}' not found in '{text}'"
