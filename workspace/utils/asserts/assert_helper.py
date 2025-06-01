import json
from typing import Any, Dict, List

def tool(func):
    """自製工具標記（供工具表用）"""
    func.is_tool = True
    return func

@tool
def assert_status_code(response: Any, expected: int):
    """驗證 response.status_code 是否等於預期 [TOOL]
    
    Args:
        response: 任何帶 status_code 屬性的物件
        expected: 預期狀態碼
    Raises:
        AssertionError: 若不等於預期
    """
    actual = getattr(response, "status_code", None)
    assert actual == expected, f"Expected status code {expected}, got {actual}"

@tool
def assert_in_keys(obj: Dict, keys: List[str]):
    """驗證 obj 是否包含所有指定 keys [TOOL]
    
    Args:
        obj: 被驗證的 dict
        keys: 必須包含的 key 名清單
    Raises:
        AssertionError: 若有缺 key
    """
    missing = [key for key in keys if key not in obj]
    assert not missing, f"Missing keys in response: {missing}"

@tool
def assert_json_equal(actual_json: Dict, expected_json: Dict):
    """驗證兩個 JSON 結構是否一致 [TOOL]
    
    Args:
        actual_json: 真實資料 dict
        expected_json: 預期資料 dict
    Raises:
        AssertionError: 若內容不同
    """
    actual_str = json.dumps(actual_json, sort_keys=True)
    expected_str = json.dumps(expected_json, sort_keys=True)
    assert actual_str == expected_str, (
        f"JSON not equal!\nActual: {actual_str}\nExpected: {expected_str}"
    )

@tool
def assert_contains_substring(text: str, substring: str):
    """驗證 substring 是否出現在 text 中 [TOOL]
    
    Args:
        text: 被檢查的主字串
        substring: 須被包含的小字串
    Raises:
        AssertionError: 若未包含
    """
    assert substring in text, f"'{substring}' not found in '{text}'"
