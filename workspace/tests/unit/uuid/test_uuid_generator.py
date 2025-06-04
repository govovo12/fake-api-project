# test_uuid_generator.py

import pytest
from workspace.utils.uuid.uuid_generator import generate_batch_uuid

pytestmark = [pytest.mark.unit, pytest.mark.uuid]

def test_uuid_format():
    """
    測試 UUID 長度與格式是否正確
    """
    uid = generate_batch_uuid()
    assert isinstance(uid, str), "UUID 應為字串"
    assert len(uid) == 32, f"UUID 長度應為 32，實際為 {len(uid)}"
    assert all(c in "0123456789abcdef" for c in uid), f"UUID 含有非 hex 字元：{uid}"

def test_uuid_uniqueness():
    """
    測試多次產生的 UUID 是否不重複
    """
    uuids = {generate_batch_uuid() for _ in range(1000)}
    assert len(uuids) == 1000, "UUID 應每次皆唯一"
