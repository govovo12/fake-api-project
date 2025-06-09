import pytest
from workspace.modules.fake_data.orchestrator.testdata_product_writer import write_product_data
from workspace.config.rules.error_codes import ResultCode

# ✅ 單元測試標記：unit + orchestrator 分類
pytestmark = [pytest.mark.unit, pytest.mark.orchestrator]


# 測試：模擬產生路徑失敗（資料夾不存在）
def test_product_dir_not_found(monkeypatch):
    mock_uuid = "abc123"

    # ✅ patch 產生路徑失敗，並給出錯誤原因
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_product_writer.generate_testdata_path",
        lambda kind, uuid: (None, {"reason": "dir_not_found_product"})
    )

    code, data, meta = write_product_data(mock_uuid, {})

    assert code == ResultCode.PRODUCT_TESTDATA_SAVE_FAILED
    assert data is None
    assert meta["reason"] == "dir_not_found_product"


# 測試：模擬寫入失敗
def test_product_save_failed(monkeypatch):
    mock_uuid = "abc123"

    # ✅ patch 產生成功路徑
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_product_writer.generate_testdata_path",
        lambda kind, uuid: (f"/mock/product_{uuid}.json", {})
    )

    # ✅ patch 寫入失敗
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_product_writer.save_json",
        lambda path, data: (False, {"reason": "save_failed_product"})
    )

    code, data, meta = write_product_data(mock_uuid, {"name": "mock"})

    assert code == ResultCode.PRODUCT_TESTDATA_FILE_WRITE_FAILED
    assert data is None
    assert meta["reason"] == "save_failed_product"


# 測試：成功寫入 product 測資
def test_product_write_success(monkeypatch):
    mock_uuid = "abc123"

    # ✅ patch 產生成功路徑
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_product_writer.generate_testdata_path",
        lambda kind, uuid: (f"/mock/product_{uuid}.json", {})
    )

    # ✅ patch 寫入成功
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_product_writer.save_json",
        lambda path, data: (True, {})
    )

    code, data, meta = write_product_data(mock_uuid, {"name": "mock"})

    assert code == ResultCode.SUCCESS
    assert isinstance(data, str)
    assert data.endswith(".json")
    assert meta is None
