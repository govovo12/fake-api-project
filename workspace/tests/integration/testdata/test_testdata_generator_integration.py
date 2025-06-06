import pytest

# 模組級標記：這支測試屬於 integration 測試 + testdata 類別
pytestmark = [pytest.mark.integration, pytest.mark.testdata]

from workspace.modules.fake_data.orchestrator import testdata_generator
from workspace.config.paths import USER_TESTDATA_ROOT as USER_PATH, PRODUCT_TESTDATA_ROOT as PRODUCT_PATH
from workspace.utils.file.file_helper import file_exists
from workspace.config.rules.error_codes import ResultCode

# ✅ 測試成功產生測資的情況
def test_generate_testdata_success():
    # 呼叫組合器，應回傳 code == 0 且包含 uuid 與測資內容
    code, result = testdata_generator.generate_testdata()

    # 驗證狀態碼與 uuid 格式
    assert code == ResultCode.SUCCESS
    assert isinstance(result, dict)
    assert isinstance(result["uuid"], str)
    assert len(result["uuid"]) > 10

    # 驗證是否正確產生對應的測資檔案（user / product）
    user_file = USER_PATH / f"{result['uuid']}.json"
    product_file = PRODUCT_PATH / f"{result['uuid']}.json"

    assert file_exists(user_file)
    assert file_exists(product_file)

# ❌ 模擬 generate_fake_user 回傳錯誤的情況，測試組合器是否正確回傳錯誤碼
def test_generate_testdata_fail_if_user_generator_fails(monkeypatch):
    # 定義 mock 版本：強制回傳錯誤碼與 None
    def mock_fail_user_generator():
        return ResultCode.USER_GENERATION_FAILED, None

    # 這裡必須 patch 組合器內實際使用的引用名稱
    # 否則會 patch 錯位置（失效）
    monkeypatch.setattr(
        testdata_generator,
        "generate_fake_user",
        mock_fail_user_generator,
    )

    # 呼叫組合器，預期應拿到錯誤碼
    code, _ = testdata_generator.generate_testdata()
    assert code == ResultCode.USER_GENERATION_FAILED
