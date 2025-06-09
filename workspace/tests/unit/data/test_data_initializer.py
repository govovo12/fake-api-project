import pytest
from pathlib import Path
from workspace.utils.data.data_initializer import write_empty_data_file, generate_empty_data

pytestmark = [pytest.mark.unit, pytest.mark.data]

def test_generate_empty_data_user():
    """
    測試 generate_empty_data 回傳 user 空資料結構
    """
    data = generate_empty_data("user")
    assert data == {
        "uuid": "",
        "name": "",
        "email": ""
    }

def test_generate_empty_data_product():
    """
    測試 generate_empty_data 回傳 product 空資料結構
    """
    data = generate_empty_data("product")
    assert data == {
        "uuid": "",
        "name": "",
        "price": 0
    }

def test_generate_empty_data_unknown_kind():
    """
    測試 generate_empty_data 傳入未知種類時回傳空 dict
    """
    data = generate_empty_data("unknown")
    assert data == {}

def test_write_empty_data_file_success(tmp_path):
    """
    測試 write_empty_data_file 正常執行並建立空檔案
    """
    path = tmp_path / "empty.json"
    success, meta = write_empty_data_file(path, "user")
    assert success is True
    assert meta == {}
    assert path.exists()
    assert path.read_text() == "{}"

def test_write_empty_data_file_save_failed(monkeypatch, tmp_path):
    def fake_save_json(path, data):
        return False, {"reason": "data_initializer_save_failed", "message": "fake error", "path": str(path), "kind": "user"}

    monkeypatch.setattr("workspace.utils.data.data_initializer.save_json", fake_save_json)
    path = tmp_path / "empty.json"
    success, meta = write_empty_data_file(path, "user")
    assert success is False
    assert meta["reason"] == "data_initializer_save_failed"
    # 只檢查 reason，message 不檢查或用 in


def test_write_empty_data_file_exception(monkeypatch, tmp_path):
    """
    模擬 save_json 拋出例外時，write_empty_data_file 應回傳失敗 reason
    """
    def fake_save_json(path, data):
        raise Exception("exception error")

    monkeypatch.setattr("workspace.utils.data.data_initializer.save_json", fake_save_json)
    path = tmp_path / "empty.json"
    success, meta = write_empty_data_file(path, "user")
    assert success is False
    assert meta["reason"] == "data_initializer_save_failed"
    assert "exception error" in meta["message"]
