import pytest
from workspace.modules.fake_data.orchestrator.testdata_user_writer import write_user_data
from workspace.config.rules.error_codes import ResultCode

# ✅ 單元測試標記
pytestmark = [pytest.mark.unit, pytest.mark.orchestrator]


# 測試：模擬資料夾不存在 → 產生路徑失敗
def test_user_dir_not_found(monkeypatch):
    mock_uuid = "abc123"

    # ✅ patch generate_testdata_path 回傳錯誤 reason
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_user_writer.generate_testdata_path",
        lambda kind, uuid: (None, {"reason": "dir_not_found_user"})
    )

    code, data, meta = write_user_data(mock_uuid, {})

    assert code == ResultCode.USER_TESTDATA_SAVE_FAILED
    assert data is None
    assert meta["reason"] == "dir_not_found_user"


# 測試：模擬寫入失敗
def test_user_save_failed(monkeypatch):
    mock_uuid = "abc123"

    # ✅ patch 成功產生路徑
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_user_writer.generate_testdata_path",
        lambda kind, uuid: (f"/mock/user_{uuid}.json", {})
    )

    # ✅ patch save_json 回傳失敗
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_user_writer.save_json",
        lambda path, data: (False, {"reason": "save_failed_user"})
    )

    code, data, meta = write_user_data(mock_uuid, {"name": "mock"})

    assert code == ResultCode.USER_TESTDATA_FILE_WRITE_FAILED
    assert data is None
    assert meta["reason"] == "save_failed_user"


# 測試：成功寫入
def test_user_write_success(monkeypatch):
    mock_uuid = "abc123"

    # ✅ patch 成功產生路徑
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_user_writer.generate_testdata_path",
        lambda kind, uuid: (f"/mock/user_{uuid}.json", {})
    )

    # ✅ patch save_json 回傳成功
    monkeypatch.setattr(
        "workspace.modules.fake_data.orchestrator.testdata_user_writer.save_json",
        lambda path, data: (True, {})
    )

    code, data, meta = write_user_data(mock_uuid, {"name": "mock"})

    assert code == ResultCode.SUCCESS
    assert isinstance(data, str)
    assert data.endswith(".json")
    assert meta is None
