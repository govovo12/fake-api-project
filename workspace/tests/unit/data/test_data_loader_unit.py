import pytest
from pathlib import Path
from utils.data import data_loader
from workspace.config.rules.error_codes import ResultCode

pytestmark = [pytest.mark.unit, pytest.mark.data]

# ✅ load_json：成功讀取合法 JSON
def test_load_json_valid_file(tmp_path):
    """✅ load_json 可正確讀取合法 JSON 檔案"""
    file = tmp_path / "valid.json"
    file.write_text('{"name": "Shopee", "level": 10}', encoding="utf-8")
    code, data = data_loader.load_json(file)
    assert code == ResultCode.SUCCESS
    assert data == {"name": "Shopee", "level": 10}

# ✅ load_json：讀取空檔案應失敗
def test_load_json_empty_file(tmp_path):
    """✅ load_json 遇空檔案應回傳錯誤碼與 None"""
    file = tmp_path / "empty.json"
    file.write_text("", encoding="utf-8")
    code, data = data_loader.load_json(file)
    assert code == ResultCode.USER_TESTDATA_NOT_FOUND
    assert data is None

# ✅ load_json：讀取格式錯誤 JSON
def test_load_json_invalid_format(tmp_path):
    """✅ load_json 遇格式錯誤 JSON 應回傳錯誤碼與 None"""
    file = tmp_path / "bad.json"
    file.write_text("{bad json}", encoding="utf-8")
    code, data = data_loader.load_json(file)
    assert code == ResultCode.USER_TESTDATA_NOT_FOUND
    assert data is None

# ✅ load_json：讀取不存在檔案
def test_load_json_file_not_exist(tmp_path):
    """✅ load_json 遇不存在檔案應回傳錯誤碼與 None"""
    file = tmp_path / "missing.json"
    code, data = data_loader.load_json(file)
    assert code == ResultCode.USER_TESTDATA_NOT_FOUND
    assert data is None

# ✅ save_json：成功儲存資料
def test_save_json_valid_data(tmp_path):
    """✅ save_json 可成功儲存合法 dict"""
    file = tmp_path / "saved.json"
    data = {"project": "fake-api", "status": "ok"}
    code = data_loader.save_json(data, file)
    assert code == ResultCode.SUCCESS
    assert file.read_text(encoding="utf-8") != ""

# ✅ save_json：資料不可序列化（如 set）
def test_save_json_invalid_data_type(tmp_path):
    """✅ save_json 遇無法轉成 JSON 的資料型別應回傳錯誤碼"""
    file = tmp_path / "invalid.json"
    data = {"bad": {1, 2, 3}}  # set 無法轉為 JSON
    code = data_loader.save_json(data, file)
    assert code == ResultCode.USER_WRITE_FAIL
    assert not file.exists() or file.read_text(encoding="utf-8") == ""

# ✅ save_json：目標目錄不存在也能自動建立
def test_save_json_create_parent_dir(tmp_path):
    """✅ save_json 可自動建立不存在的上層資料夾"""
    target = tmp_path / "deep" / "nested" / "data.json"
    data = {"deep": "ok"}
    code = data_loader.save_json(data, target)
    assert code == ResultCode.SUCCESS
    assert target.exists()
