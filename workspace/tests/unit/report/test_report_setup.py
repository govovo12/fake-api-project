import pytest
import re
from pathlib import Path
from workspace.scripts import report_setup
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.report]

# ----------------------
# 測試用共用變數
# ----------------------
VALID_PHASE = "unit"


# ----------------------
# ✅ 正向測試
# ----------------------
def test_get_timestamped_report_path_success(tmp_path, monkeypatch):
    """
    ✅ 正向測試：檢查報告路徑是否正確產出，並符合命名格式
    """
    monkeypatch.setattr(report_setup, "get_report_dir", lambda: tmp_path)
    monkeypatch.setattr(report_setup, "ensure_dir", lambda path: ResultCode.SUCCESS)
    monkeypatch.setattr(report_setup, "delete_file", lambda path: ResultCode.SUCCESS)

    path = report_setup.get_timestamped_report_path(phase=VALID_PHASE)

    # 檢查子資料夾是否正確
    assert tmp_path / VALID_PHASE in path.parents

    # 檢查檔名格式正確
    assert re.match(rf"{VALID_PHASE}_test_report_\d{{4}}-\d{{2}}-\d{{2}}-\d{{2}}-\d{{2}}\.html", path.name)


# ----------------------
# ❌ 例外處理測試
# ----------------------
def test_prepare_report_directory_fail(tmp_path, monkeypatch):
    """
    ❌ 負向測試：模擬建立資料夾失敗時，應拋出 RuntimeError
    """
    monkeypatch.setattr(report_setup, "get_report_dir", lambda: tmp_path)
    monkeypatch.setattr(report_setup, "ensure_dir", lambda path: ResultCode.TOOL_DIR_CREATE_FAILED)

    with pytest.raises(RuntimeError, match="建立報告資料夾失敗"):
        report_setup.get_timestamped_report_path(phase=VALID_PHASE)


# ----------------------
# ⚠ 刪除失敗測試
# ----------------------
def test_prepare_report_directory_delete_fail_warning(tmp_path, monkeypatch, capsys):
    """
    ⚠ 邊界測試：模擬 delete_file 失敗，應印出 warning 但不拋出例外
    """
    html_file = tmp_path / VALID_PHASE / "old_report.html"
    html_file.parent.mkdir(parents=True, exist_ok=True)
    html_file.touch()

    monkeypatch.setattr(report_setup, "get_report_dir", lambda: tmp_path)
    monkeypatch.setattr(report_setup, "ensure_dir", lambda path: ResultCode.SUCCESS)
    monkeypatch.setattr(report_setup, "delete_file", lambda path: ResultCode.TOOL_FILE_DELETE_FAILED)


    report_setup.get_timestamped_report_path(phase=VALID_PHASE)

    captured = capsys.readouterr()
    assert "無法刪除舊報告" in captured.out


# ----------------------
# ✅ 邊界測試：空資料夾也可成功
# ----------------------
def test_prepare_report_directory_empty(tmp_path, monkeypatch):
    """
    ✅ 邊界測試：phase 資料夾為空，仍可成功建立新報告
    """
    monkeypatch.setattr(report_setup, "get_report_dir", lambda: tmp_path)
    monkeypatch.setattr(report_setup, "ensure_dir", lambda path: ResultCode.SUCCESS)
    monkeypatch.setattr(report_setup, "delete_file", lambda path: ResultCode.SUCCESS)

    path = report_setup.get_timestamped_report_path(phase=VALID_PHASE)
    assert path.exists() is False  # pytest-html 尚未寫入前，應不存在，但路徑應合法
