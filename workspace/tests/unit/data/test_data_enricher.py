import pytest
from workspace.utils.data.data_enricher import enrich_with_uuid, enrich_payload

# ✅ 全檔標記：unit + data
pytestmark = [pytest.mark.unit, pytest.mark.data]


def test_enrich_with_uuid_success():
    """
    ✅ 測試 UUID 注入成功（回傳新 dict）
    """
    data = {"name": "Alice"}
    success, new_data, meta = enrich_with_uuid(data, "abc-123")
    assert success is True
    assert new_data["uuid"] == "abc-123"
    assert new_data["name"] == "Alice"
    assert meta is None
    assert "uuid" not in data  # ✅ 原 dict 不應被修改


def test_enrich_with_uuid_not_dict():
    """
    ✅ 測試傳入非 dict，回傳錯誤 reason
    """
    success, new_data, meta = enrich_with_uuid("not a dict", "abc-123")
    assert success is False
    assert new_data is None
    assert meta["reason"] == "not_a_dict"


def test_enrich_with_uuid_exception():
    """
    ✅ 測試模擬 data.copy() 發生例外
    """
    class FakeBadData(dict):
        def copy(self):
            raise Exception("copy failed")

    bad_data = FakeBadData()
    success, new_data, meta = enrich_with_uuid(bad_data, "xyz")
    assert success is False
    assert meta["reason"] == "enrich_failed"
    assert "copy failed" in meta["message"]



def test_enrich_payload_basic():
    """
    ✅ 測試 enrich_payload 擷取指定欄位資料
    """
    data = {"name": "Alice", "email": "a@b.com"}
    result = enrich_payload(data, "name,email")
    assert result == {"name": "Alice", "email": "a@b.com"}


def test_enrich_payload_partial_key():
    """
    ✅ 測試 enrich_payload 忽略不存在欄位
    """
    data = {"name": "Alice"}
    result = enrich_payload(data, "name,email")  # email 不存在
    assert result == {"name": "Alice", "email": None}


def test_enrich_payload_trim_spaces():
    """
    ✅ 測試欄位有空格仍能正確抓取
    """
    data = {"x": 1, "y": 2}
    result = enrich_payload(data, " x , y ")
    assert result == {"x": 1, "y": 2}
