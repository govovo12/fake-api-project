import pytest
from workspace.utils.uuid.uuid_generator import generate_batch_uuid_with_code

pytestmark = [pytest.mark.unit, pytest.mark.uuid]


def test_generate_uuid_success():
    """
    測試成功產生 UUID，應該回傳 success=True 且 UUID 為 hex 字串
    """
    success, uuid, meta = generate_batch_uuid_with_code()
    assert success is True
    assert isinstance(uuid, str)
    assert len(uuid) == 32
    assert all(c in "0123456789abcdef" for c in uuid)
    assert meta is None


def test_generate_uuid_fail(monkeypatch):
    """
    模擬 uuid.uuid4 發生例外，應該回傳 success=False 且 meta 含錯誤訊息
    """
    import uuid
    monkeypatch.setattr(uuid, "uuid4", lambda: (_ for _ in ()).throw(Exception("mock error")))

    success, uuid, meta = generate_batch_uuid_with_code()
    assert success is False
    assert uuid is None
    assert meta is not None
    assert meta.get("reason") == "uuid_generate_failed"
    assert "mock error" in meta.get("message", "")
