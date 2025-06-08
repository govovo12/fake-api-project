import pytest
import json
from pathlib import Path
from workspace.utils.file import file_helper

pytestmark = [pytest.mark.unit, pytest.mark.data]

# ✅ 測試：建立目錄
def test_ensure_dir_creates_directory(tmp_path):
    path = tmp_path / "new_dir"
    assert not path.exists()
    file_helper.ensure_dir(path)
    assert path.exists()
    assert path.is_dir()

# ✅ 測試：建立空檔案
def test_ensure_file_creates_file(tmp_path):
    file_path = tmp_path / "file.json"
    assert not file_path.exists()
    file_helper.ensure_file(file_path)
    assert file_path.exists()
    assert file_path.is_file()

# ✅ 測試：檔案存在時應回傳 True
def test_file_exists_returns_true(tmp_path):
    file_path = tmp_path / "existing.json"
    file_path.write_text("test")
    assert file_helper.file_exists(file_path) is True

# ✅ 測試：檔案不存在時應回傳 False
def test_file_exists_returns_false(tmp_path):
    file_path = tmp_path / "missing.json"
    assert file_helper.file_exists(file_path) is False

# ✅ 測試：成功讀取 json 檔
def test_load_json_loads_data(tmp_path):
    file_path = tmp_path / "data.json"
    data = {"name": "Alice"}
    file_path.write_text(json.dumps(data))
    result = file_helper.load_json(file_path)
    assert result == data

# ✅ 測試：讀取格式錯誤的 json 應回傳 None
def test_load_json_returns_none_on_invalid_json(tmp_path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text("not json")
    result = file_helper.load_json(file_path)
    assert result is None

# ✅ 修正：測試 json 寫入是否成功
def test_save_json_writes_data(tmp_path):
    """
    ✅ 測試：正常儲存 JSON 檔案，並驗證內容正確
    """
    file_path = tmp_path / "output.json"
    data = {"x": 1}

    success, meta = file_helper.save_json(file_path, data)

    assert success is True, f"❌ 儲存失敗，錯誤資訊：{meta}"
    assert meta is None
    assert file_path.exists(), "❌ 檔案未正確建立"
    
    content = file_path.read_text()
    assert json.loads(content) == data


# ✅ 測試：寫入不可序列化物件應失敗
def test_save_json_handles_non_serializable(tmp_path):
    """
    ✅ 測試：儲存無法序列化的資料應失敗，並提供錯誤 meta
    """
    file_path = tmp_path / "fail.json"

    class NonSerializable:
        pass

    success, meta = file_helper.save_json(file_path, {"obj": NonSerializable()})

    assert success is False, "❌ 預期失敗，但成功"
    assert meta is not None
    assert meta["reason"] == "json_serialization_failed", f"❌ 錯誤原因錯誤，實際為：{meta['reason']}"


# ✅ 修正：測試建立暫存檔案
def test_write_temp_file_creates_file():
    content = "test content"
    temp_file = file_helper.write_temp_file("x", content)
    assert temp_file.exists()
    assert temp_file.read_text() == content

# ✅ 修正：測試刪除存在的檔案
def test_clear_file_removes_existing(tmp_path):
    file_path = tmp_path / "file.json"
    file_helper.ensure_file(file_path)
    assert file_path.exists()
    file_helper.clear_file(file_path)
    assert not file_path.exists()

# ✅ 測試：刪除不存在的檔案不應報錯
def test_clear_file_ignores_missing(tmp_path):
    file_path = tmp_path / "missing.json"
    assert not file_path.exists()
    file_helper.clear_file(file_path)  # 不應 raise error

# ✅ 測試：正常組出測資儲存路徑
def test_get_testdata_file_path_success(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    success, path, meta = file_helper.get_testdata_file_path("user", "abc-123")
    assert success is True
    assert meta is None
    assert isinstance(path, Path)
    assert path.name == "abc-123.json"
    assert "user" in str(path)

# ✅ 測試：錯誤類型應回報 invalid_kind
def test_get_testdata_file_path_invalid_kind():
    success, path, meta = file_helper.get_testdata_file_path("dog", "abc-123")
    assert not success
    assert path is None
    assert meta["reason"] == "invalid_kind"

# ✅ 測試：uuid 為 None 或空字串應回報 invalid_uuid
def test_get_testdata_file_path_invalid_uuid():
    success, path, meta = file_helper.get_testdata_file_path("user", None)
    assert not success
    assert meta["reason"] == "invalid_uuid"

    success2, path2, meta2 = file_helper.get_testdata_file_path("user", "")
    assert not success2
    assert meta2["reason"] == "invalid_uuid"

# ✅ 測試：模擬 mkdir 失敗，應回報 path_generation_failed
def test_get_testdata_file_path_fail_mkdir(monkeypatch):
    def mock_mkdir_fail(*args, **kwargs):
        raise OSError("mock mkdir failed")
    monkeypatch.setattr(Path, "mkdir", mock_mkdir_fail)
    success, path, meta = file_helper.get_testdata_file_path("user", "abc")
    assert not success
    assert meta["reason"] == "path_generation_failed"
    assert "mock" in meta["message"]
