import pytest
import uuid

# ✅ 測試標記：單元測試 + uuid 分類
pytestmark = [pytest.mark.unit, pytest.mark.uuid]

from workspace.utils.uuid.uuid_generator import (
    generate_uuid,
    generate_batch_uuid_with_code,
)
from workspace.config.rules.error_codes import TaskModuleError


def test_generate_uuid_success():
    """
    正向測試：generate_uuid 應成功產生 32 位數的 UUID 字串
    """
    result = generate_uuid()
    assert isinstance(result, str)
    assert len(result) == 32
    assert all(c in "0123456789abcdef" for c in result)


def test_generate_batch_uuid_success():
    """
    正向測試：generate_batch_uuid_with_code 應成功產生 32 位數的 UUID 字串
    """
    result = generate_batch_uuid_with_code()
    assert isinstance(result, str)
    assert len(result) == 32
    assert all(c in "0123456789abcdef" for c in result)


def test_generate_batch_uuid_uniqueness():
    """
    邊界測試：連續產生 100 組 UUID，應無重複值
    """
    uuids = {generate_batch_uuid_with_code() for _ in range(100)}
    assert len(uuids) == 100


def test_generate_batch_uuid_fail_by_monkeypatch(monkeypatch):
    """
    異常模擬：模擬 uuid.uuid4 發生例外時，應正確拋出 TaskModuleError
    """
    def broken_uuid():
        raise Exception("UUID system failure")

    monkeypatch.setattr(uuid, "uuid4", broken_uuid)

    with pytest.raises(TaskModuleError) as e:
        generate_batch_uuid_with_code()
