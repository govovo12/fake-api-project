import pytest
from workspace.utils.uuid.uuid_generator import generate_batch_uuid_with_code
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.uuid]

def test_uuid_with_code_success():
    """
    測試 UUID 產生成功的情境
    """
    code, uid = generate_batch_uuid_with_code()
    assert code == ResultCode.SUCCESS, f"應回傳成功 code=0，實際為 {code}"
    assert isinstance(uid, str), "UUID 應為字串"
    assert len(uid) == 32, f"UUID 長度應為 32，實際為 {len(uid)}"
    assert all(c in "0123456789abcdef" for c in uid), f"UUID 含有非 hex 字元：{uid}"

def test_uuid_with_code_uniqueness():
    """
    測試多次產生的 UUID 是否唯一且成功
    """
    results = [generate_batch_uuid_with_code() for _ in range(1000)]
    codes = [code for code, _ in results]
    uuids = [uid for _, uid in results]
    assert all(code == ResultCode.SUCCESS for code in codes), "所有產生應該都成功"
    assert len(set(uuids)) == 1000, "UUID 應每次皆唯一"

def test_uuid_with_code_fail(monkeypatch):
    """
    模擬 uuid.uuid4 發生例外，應回傳 UUID_GEN_FAIL 且為 None
    """
    import workspace.utils.uuid.uuid_generator as uuid_gen

    def mock_uuid4_fail():
        raise Exception("故意觸發錯誤")

    monkeypatch.setattr("uuid.uuid4", mock_uuid4_fail)
    code, uid = uuid_gen.generate_batch_uuid_with_code()
    assert code == ResultCode.UUID_GEN_FAIL, f"應回傳 UUID_GEN_FAIL，實際為 {code}"
    assert uid is None, "失敗時 UUID 應為 None"

