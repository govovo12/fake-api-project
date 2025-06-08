# test_data_enricher_unit.py

import pytest
from workspace.utils.data.data_enricher import enrich_with_uuid

pytestmark = [pytest.mark.unit, pytest.mark.data]

def test_enrich_with_uuid_adds_uuid():
    data = {"a": 1}
    uuid = "abc-123"
    success, result, meta = enrich_with_uuid(data, uuid)
    assert success is True
    assert meta is None
    assert result == {"a": 1, "uuid": "abc-123"}

def test_enrich_with_uuid_on_empty_dict():
    data = {}
    uuid = "x"
    success, result, meta = enrich_with_uuid(data, uuid)
    assert success is True
    assert result == {"uuid": "x"}

def test_enrich_with_uuid_does_not_modify_original():
    data = {"k": 5}
    uuid = "test"
    _success, result, _meta = enrich_with_uuid(data, uuid)
    assert data == {"k": 5}
    assert result != data

def test_enrich_with_uuid_override_existing_uuid():
    data = {"uuid": "old"}
    uuid = "new"
    success, result, meta = enrich_with_uuid(data, uuid)
    assert success is True
    assert result["uuid"] == "new"

def test_enrich_with_uuid_various_types():
    data = {"x": [1, 2], "y": None}
    uuid = "xx"
    success, result, meta = enrich_with_uuid(data, uuid)
    assert success is True
    assert result == {"x": [1, 2], "y": None, "uuid": "xx"}

def test_enrich_with_uuid_large_dict():
    data = {str(i): i for i in range(1000)}
    uuid = "LARGE"
    success, result, meta = enrich_with_uuid(data, uuid)
    assert success is True
    assert result["uuid"] == uuid
    assert len(result) == 1001
    for i in range(1000):
        assert result[str(i)] == i

def test_enrich_with_uuid_uuid_accepts_any_type():
    data = {"foo": "bar"}
    uuid = 123  # 非字串，但工具模組不做限制
    success, result, meta = enrich_with_uuid(data, uuid)
    assert success is True
    assert result["uuid"] == 123

def test_enrich_with_uuid_invalid_data_type():
    success, result, meta = enrich_with_uuid(["not", "a", "dict"], "abc")
    assert success is False
    assert result is None
    assert meta["reason"] == "not_a_dict"

def test_enrich_with_uuid_unexpected_exception(monkeypatch):
    class BrokenDict(dict):
        def copy(self):
            raise RuntimeError("mock error")

    broken_data = BrokenDict(name="test")
    success, result, meta = enrich_with_uuid(broken_data, "uuid-xyz")

    assert success is False
    assert result is None
    assert meta["reason"] == "enrich_failed"
    assert "mock error" in meta["message"]

def test_enrich_with_uuid_dict_with_special_types():
    class CustomObj:
        def __init__(self, value):
            self.value = value
    data = {"obj": CustomObj("a")}
    uuid = "custom"
    success, result, meta = enrich_with_uuid(data, uuid)
    assert success is True
    assert result["uuid"] == uuid
