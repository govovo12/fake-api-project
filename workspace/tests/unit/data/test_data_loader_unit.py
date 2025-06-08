# test_data_loader.py

import pytest
import json
from pathlib import Path
from workspace.utils.data.data_loader import save_json, load_json
from workspace.utils.file import file_helper
pytestmark = [pytest.mark.unit, pytest.mark.data]

def test_save_json_success(tmp_path):
    """
    測試：成功寫入 JSON 檔案
    """
    test_path = tmp_path / "data.json"
    success, meta = save_json({"key": "value"}, test_path)
    assert success is True
    assert meta is None
    assert test_path.exists()


def test_save_json_fail_permission(monkeypatch):
    """
    測試：模擬 PermissionError 錯誤
    """
    def raise_permission(*args, **kwargs):
        raise PermissionError("mock no permission")

    monkeypatch.setattr(file_helper, "save_json", raise_permission)
    success, meta = save_json({"a": 1}, "mock_path.json")
    assert success is False
    assert meta["reason"] == "permission_denied"
    assert "mock" in meta["message"]


def test_load_json_success(tmp_path):
    """
    測試：成功讀取 JSON 檔案
    """
    test_path = tmp_path / "data.json"
    test_data = {"k": 1}
    test_path.write_text(json.dumps(test_data), encoding="utf-8")

    success, data, meta = load_json(test_path)
    assert success is True
    assert data == test_data
    assert meta is None


def test_load_json_file_not_found():
    """
    測試：檔案不存在的處理
    """
    success, data, meta = load_json("non_existent_file.json")
    assert success is False
    assert data is None
    assert meta["reason"] == "file_not_found"
