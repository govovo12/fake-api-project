import pytest
from pathlib import Path
from utils.file.file_helper import (
    ensure_dir, ensure_file, file_exists, get_file_name_from_path,
    is_file_empty, clear_file, write_temp_file,
    load_json, save_json
)

pytestmark = [pytest.mark.unit, pytest.mark.file]

# ✅ ensure_dir: 建立不存在的資料夾
def test_ensure_dir_creates_directory(tmp_path):
    """✅ ensure_dir 可建立不存在的資料夾"""
    d = tmp_path / "mydir"
    assert not d.exists()
    ensure_dir(d)
    assert d.exists() and d.is_dir()

# ✅ ensure_file: 建立檔案與其上層資料夾
def test_ensure_file_creates_file_and_parents(tmp_path):
    """✅ ensure_file 可建立檔案與上層資料夾"""
    f = tmp_path / "abc" / "test.txt"
    assert not f.exists()
    ensure_file(f)
    assert f.exists() and f.is_file()

# ✅ file_exists: 檢查檔案是否存在
def test_file_exists_true_and_false(tmp_path):
    """✅ file_exists 可正確判斷存在與不存在的檔案"""
    f = tmp_path / "a.txt"
    assert not file_exists(f)
    f.write_text("data")
    assert file_exists(f)

# ✅ get_file_name_from_path: 擷取檔名
def test_get_file_name_from_path(tmp_path):
    """✅ get_file_name_from_path 可取得檔名"""
    f = tmp_path / "dir1" / "myfile.csv"
    ensure_dir(f.parent)
    f.write_text("123")
    name = get_file_name_from_path(f)
    assert name == "myfile.csv"

# ✅ is_file_empty: 檢查是否為空檔
def test_is_file_empty_true_and_false(tmp_path):
    """✅ is_file_empty 可判斷空檔與非空檔"""
    f = tmp_path / "test.txt"
    ensure_file(f)
    assert is_file_empty(f)
    f.write_text("abc", encoding="utf-8")
    assert not is_file_empty(f)

# ✅ clear_file: 清空檔案內容（若檔案存在）
def test_clear_file(tmp_path):
    """✅ clear_file 可清空檔案內容"""
    f = tmp_path / "clear.txt"
    f.write_text("hello", encoding="utf-8")
    clear_file(f)
    assert is_file_empty(f)

    # 不存在的檔案呼叫 clear_file 不應報錯
    f2 = tmp_path / "no.txt"
    clear_file(f2)  # 不報錯即為通過

# ✅ write_temp_file: 寫入暫存檔案並確認內容與副檔名
def test_write_temp_file_and_content():
    """✅ write_temp_file 寫入內容後可正確存取"""
    content = "Hello, Shopee!"
    temp_path = write_temp_file(content, suffix=".dat")
    assert temp_path.exists()
    assert temp_path.read_text(encoding="utf-8") == content
    assert temp_path.suffix == ".dat"

# ✅ load_json: 讀取合法 JSON 檔案
def test_load_json_success(tmp_path):
    """✅ load_json 可正確讀取合法 JSON 檔案"""
    data = {"name": "Tony", "level": 14}
    json_path = tmp_path / "data.json"
    json_path.write_text('{"name": "Tony", "level": 14}', encoding="utf-8")
    result = load_json(json_path)
    assert result == data

# ✅ load_json: 讀取錯誤格式 JSON 回傳 None
def test_load_json_invalid_returns_none(tmp_path):
    """✅ load_json 讀取錯誤格式 JSON 應回傳 None"""
    path = tmp_path / "bad.json"
    path.write_text("{not valid json}", encoding="utf-8")
    result = load_json(path)
    assert result is None

# ✅ save_json: 儲存 dict 成功並可讀回
def test_save_json_success_and_validate(tmp_path):
    """✅ save_json 可成功寫入 JSON 檔並可驗證內容"""
    data = {"hello": "world"}
    path = tmp_path / "saved.json"
    success = save_json(data, path)
    assert success
    assert load_json(path) == data

# ✅ save_json: 嘗試寫入不可序列化資料（如 set）
def test_save_json_invalid_type_should_fail(tmp_path):
    """✅ save_json 遇無法序列化資料型別應失敗"""
    data = {"invalid": {1, 2, 3}}  # set 無法轉 JSON
    path = tmp_path / "bad.json"
    success = save_json(data, path)
    assert not success

# ✅ save_json: 自動建立上層目錄
def test_save_json_creates_parent_directory(tmp_path):
    """✅ save_json 可自動建立不存在的上層資料夾"""
    path = tmp_path / "deep" / "dir" / "config.json"
    data = {"deep": "structure"}
    success = save_json(data, path)
    assert success
    assert path.exists()
    assert load_json(path) == data
