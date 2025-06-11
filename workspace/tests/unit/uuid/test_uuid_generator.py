import pytest
from workspace.utils.uuid.uuid_generator import generate_batch_uuid_with_code, generate_uuid
from workspace.config.rules.error_codes import ResultCode

# 標記單元測試及 uuid 測試
pytestmark = [pytest.mark.unit, pytest.mark.uuid]

# ===============================
# 測試 generate_batch_uuid_with_code 函式
# ===============================

def test_generate_batch_uuid_with_code_success():
    """
    測試 generate_batch_uuid_with_code 函式：成功生成 UUID
    """
    result = generate_batch_uuid_with_code()
    
    # 確認返回的值是 32 字符的合法 UUID 字串
    assert len(result) == 32
    assert all(c in '0123456789abcdef' for c in result)  # 檢查是否為十六進制字符


def test_generate_batch_uuid_with_code_failure(mocker):
    """
    測試 generate_batch_uuid_with_code 函式：生成 UUID 失敗
    模擬錯誤並檢查錯誤回報
    """
    # 模擬 uuid.uuid4().hex 引發異常
    mocker.patch("uuid.uuid4", side_effect=Exception("UUID generation failed"))

    result = generate_batch_uuid_with_code()
    
    # 確認返回的錯誤代碼
    assert result == ResultCode.UUID_GEN_FAIL


# ===============================
# 測試 generate_uuid 函式
# ===============================

def test_generate_uuid_success():
    """
    測試 generate_uuid 函式：成功生成 UUID
    """
    result = generate_uuid()
    
    # 確認返回的值是 32 字符的合法 UUID 字串
    assert len(result) == 32
    assert all(c in '0123456789abcdef' for c in result)  # 檢查是否為十六進制字符


def test_generate_uuid_failure(mocker):
    """
    測試 generate_uuid 函式：生成 UUID 失敗
    模擬錯誤並檢查錯誤回報
    """
    # 模擬 uuid.uuid4().hex 引發異常
    mocker.patch("uuid.uuid4", side_effect=Exception("UUID generation failed"))

    result = generate_uuid()
    
    # 確認返回的錯誤代碼
    assert result == ResultCode.UUID_GEN_FAIL
