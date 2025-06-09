import pytest
from workspace.modules.fake_data.orchestrator.testdata_file_preparer import prepare_testdata_files
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.orchestrator]


# ✅ 成功流程：建立 user 與 product 檔案
def test_prepare_testdata_success(monkeypatch):
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_file_preparer.generate_testdata_path",
        lambda kind, uuid: (f"/mock/{kind}_{uuid}.json", {})
    )
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_file_preparer.file_exists",
        lambda path: False
    )
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_file_preparer.write_empty_data_file",
        lambda path, kind: (True, {})
    )

    code, data, meta = prepare_testdata_files("abc123")
    assert code == ResultCode.SUCCESS
    assert "user_testdata_path" in data
    assert "product_testdata_path" in data
    assert meta is None


# ❌ 模擬 user 寫入失敗
def test_write_user_file_failed(monkeypatch):
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_file_preparer.generate_testdata_path",
        lambda kind, uuid: (f"/mock/{kind}_{uuid}.json", {})
    )
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_file_preparer.file_exists",
        lambda path: False
    )

    def custom_write(path, kind):
        if "user" in path:
            return False, {"reason": "save_failed_user"}
        return True, {}

    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_file_preparer.write_empty_data_file",
        custom_write
    )

    code, data, meta = prepare_testdata_files("abc123")
    assert code == ResultCode.USER_TESTDATA_FILE_WRITE_FAILED


# ❌ 模擬 product 寫入失敗
def test_write_product_file_failed(monkeypatch):
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_file_preparer.generate_testdata_path",
        lambda kind, uuid: (f"/mock/{kind}_{uuid}.json", {})
    )
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_file_preparer.file_exists",
        lambda path: False
    )

    def custom_write(path, kind):
        if "product" in path:
            return False, {"reason": "save_failed_product"}
        return True, {}

    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_file_preparer.write_empty_data_file",
        custom_write
    )

    code, data, meta = prepare_testdata_files("abc123")
    assert code == ResultCode.PRODUCT_TESTDATA_FILE_WRITE_FAILED
