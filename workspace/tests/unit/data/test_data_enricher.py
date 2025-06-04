import pytest
from workspace.utils.data.data_enricher import enrich_with_uuid

# 測試標記：屬於單元測試（unit）與資料處理（data）
pytestmark = [pytest.mark.unit, pytest.mark.data]

def test_enrich_with_uuid_adds_uuid():
    """
    [單元] enrich_with_uuid 基本行為測試：會正確加上 uuid 欄位
    """
    data = {"a": 1}
    uuid = "abc-123"
    result = enrich_with_uuid(data, uuid)
    assert result == {"a": 1, "uuid": "abc-123"}

def test_enrich_with_uuid_on_empty_dict():
    """
    [邊界] 傳入空 dict 也能正確加上 uuid
    """
    data = {}
    uuid = "x"
    result = enrich_with_uuid(data, uuid)
    assert result == {"uuid": "x"}

def test_enrich_with_uuid_does_not_modify_original():
    """
    [正向] 原始資料不會被修改（immutable 測試）
    """
    data = {"k": 5}
    uuid = "test"
    _ = enrich_with_uuid(data, uuid)
    assert data == {"k": 5}

def test_enrich_with_uuid_override_existing_uuid():
    """
    [反向] 若原本就有 uuid 欄位，會被覆蓋為新值
    """
    data = {"uuid": "old"}
    uuid = "new"
    result = enrich_with_uuid(data, uuid)
    assert result == {"uuid": "new"}

def test_enrich_with_uuid_various_types():
    """
    [結構性] 支援各種 value 型態，不限 key/value 內容
    """
    data = {"x": [1, 2], "y": None}
    uuid = "xx"
    result = enrich_with_uuid(data, uuid)
    assert result == {"x": [1, 2], "y": None, "uuid": "xx"}

def test_enrich_with_uuid_large_dict():
    """
    [邊界] 大型 dict 也能正確加 uuid
    """
    data = {str(i): i for i in range(1000)}
    uuid = "LARGE"
    result = enrich_with_uuid(data, uuid)
    assert result["uuid"] == "LARGE"
    assert len(result) == 1001
    # 確保原始 1000 keys 都沒變
    for i in range(1000):
        assert result[str(i)] == i

def test_enrich_with_uuid_uuid_type_is_string():
    """
    [型別] uuid 參數必須是字串型態，否則也能被正確存入（這是 Python 弱型別行為，非強制）
    """
    data = {"foo": "bar"}
    uuid = 123  # 非字串，但 Python 允許
    result = enrich_with_uuid(data, uuid)
    assert result["uuid"] == 123
