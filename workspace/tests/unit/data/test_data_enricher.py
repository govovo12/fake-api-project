import pytest
from workspace.utils.data.data_enricher import enrich_with_uuid, enrich_payload

# ✅ 測試標記：屬於單元測試 + data 類型模組
pytestmark = [pytest.mark.unit, pytest.mark.data]


def test_enrich_with_uuid_success():
    """
    測試 enrich_with_uuid：正常情況應加上 uuid 欄位並成功回傳
    """
    input_data = {"name": "Alice", "email": "alice@example.com"}
    uuid = "abc-123"
    success, enriched, meta = enrich_with_uuid(input_data, uuid)
    assert success is True
    assert meta is None
    assert enriched["uuid"] == uuid
    assert enriched["name"] == "Alice"


def test_enrich_with_uuid_input_not_dict():
    """
    測試 enrich_with_uuid：若傳入非 dict 應回傳錯誤 reason
    """
    input_data = "not a dict"
    uuid = "abc-123"
    success, enriched, meta = enrich_with_uuid(input_data, uuid)
    assert success is False
    assert enriched is None
    assert meta["reason"] == "data_enricher_not_a_dict"


def test_enrich_with_uuid_raises_exception(monkeypatch):
    """
    模擬 data.copy() 發生錯誤 → 應回傳 enrich 失敗 reason
    """
    class BrokenDict(dict):
        def copy(self):
            raise Exception("copy failed")

    data = BrokenDict({"a": 1})
    success, enriched, meta = enrich_with_uuid(data, "uuid-123")
    assert not success
    assert meta["reason"] == "data_enricher_failed"
    assert "copy failed" in meta["message"]


def test_enrich_payload_extract_fields():
    """
    測試 enrich_payload 可根據逗號欄位字串正確取出對應欄位值
    """
    data = {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30
    }
    result = enrich_payload(data, "name,email")
    assert result == {
        "name": "Alice",
        "email": "alice@example.com"
    }

def test_enrich_payload_empty_fields():
    """
    測試 enrich_payload 傳入空欄位字串應回傳空 dict
    """
    data = {"a": 1}
    result = enrich_payload(data, "")
    assert result == {}
