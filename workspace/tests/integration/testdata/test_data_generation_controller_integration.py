import pytest
from workspace.controller.data_generation_controller import generate_user_and_product_data
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.integration, pytest.mark.controller]

def test_integrated_all_success():
    """
    整合測試：兩組合器都成功 → 回傳 TESTDATA_TASK_SUCCESS
    """
    uuid = "1234567890abcdef1234567890abcdef"
    result = generate_user_and_product_data(uuid)
    assert result == ResultCode.TESTDATA_TASK_SUCCESS

def test_integrated_user_fail(monkeypatch):
    """
    整合測試：user 組合器失敗 → 中斷流程，不執行 product
    """
    from workspace.modules.fake_data.orchestrator.build_user_data_and_write import build_user_data_and_write

    def fake_user_fail(uuid):
        return ResultCode.FAKER_GENERATE_FAILED

    monkeypatch.setattr("workspace.modules.fake_data.orchestrator.build_user_data_and_write.build_user_data_and_write", fake_user_fail)

    result = generate_user_and_product_data("abc123")
    assert result == ResultCode.FAKER_GENERATE_FAILED

def test_integrated_product_fail(monkeypatch):
    """
    整合測試：user 成功但 product 失敗 → 回傳 product 錯誤碼
    """
    from workspace.modules.fake_data.orchestrator.build_product_data_and_write import build_product_data_and_write

    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.build_user_data_and_write.build_user_data_and_write",
        lambda uuid: ResultCode.SUCCESS
    )

    def fake_product_fail(uuid):
        return ResultCode.PRODUCT_GENERATION_FAILED

    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.build_product_data_and_write.build_product_data_and_write",
        fake_product_fail
    )

    result = generate_user_and_product_data("abc123")
    assert result == ResultCode.PRODUCT_GENERATION_FAILED
