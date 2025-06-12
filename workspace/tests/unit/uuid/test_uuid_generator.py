import pytest
from workspace.utils.uuid.uuid_generator import generate_batch_uuid_with_code
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.uuid]

def test_generate_batch_uuid_success():
    """
    成功產出單一 UUID，應為 32 字元十六進位字串。
    """
    result = generate_batch_uuid_with_code()
    assert isinstance(result, str)
    assert len(result) == 32
    assert all(c in "0123456789abcdef" for c in result)

def test_generate_batch_uuid_mocked_fail(monkeypatch):
    """
    模擬 uuid4 發生例外，應回傳 UUID_GEN_FAIL 錯誤碼。
    """
    import uuid

    def raise_exception():
        raise Exception("UUID fail")

    monkeypatch.setattr(uuid, "uuid4", raise_exception)

    result = generate_batch_uuid_with_code()
    assert result == ResultCode.UUID_GEN_FAIL
