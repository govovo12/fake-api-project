import pytest
from pathlib import Path
from utils.file.file_helper import (
    ensure_dir, ensure_file, file_exists, get_file_name_from_path,
    is_file_empty, clear_file, write_temp_file
)

pytestmark = [pytest.mark.unit, pytest.mark.file]

def test_ensure_dir_creates_directory(tmp_path):
    """ensure_dir 可建立不存在的資料夾"""
    d = tmp_path / "mydir"
    assert not d.exists()
    ensure_dir(d)
    assert d.exists() and d.is_dir()

def test_ensure_file_creates_file_and_parents(tmp_path):
    """ensure_file 可建立檔案與上層資料夾"""
    f = tmp_path / "abc" / "test.txt"
    assert not f.exists()
    ensure_file(f)
    assert f.exists() and f.is_file()

def test_file_exists_true_and_false(tmp_path):
    """file_exists 可正確判斷存在與不存在的檔案"""
    f = tmp_path / "a.txt"
    assert not file_exists(f)
    f.write_text("data")
    assert file_exists(f)

def test_get_file_name_from_path(tmp_path):
    """get_file_name_from_path 可取得檔名"""
    f = tmp_path / "dir1" / "myfile.csv"
    ensure_dir(f.parent)
    f.write_text("123")
    name = get_file_name_from_path(f)
    assert name == "myfile.csv"

def test_is_file_empty_true_and_false(tmp_path):
    """is_file_empty 可判斷空檔與非空檔"""
    f = tmp_path / "test.txt"
    ensure_file(f)
    assert is_file_empty(f)
    f.write_text("abc", encoding="utf-8")
    assert not is_file_empty(f)

def test_clear_file(tmp_path):
    """clear_file 可清空檔案內容"""
    f = tmp_path / "clear.txt"
    f.write_text("hello", encoding="utf-8")
    clear_file(f)
    assert is_file_empty(f)
    # 不存在的檔案呼叫 clear_file 也不報錯
    f2 = tmp_path / "no.txt"
    clear_file(f2)

def test_write_temp_file_and_content(tmp_path):
    """write_temp_file 寫入內容後可正確存取"""
    content = "Hello, Shopee!"
    temp_path = write_temp_file(content, suffix=".dat")
    assert temp_path.exists()
    assert temp_path.read_text(encoding="utf-8") == content
    assert temp_path.suffix == ".dat"
def test_clear_dir_files(tmp_path):
    """clear_dir_files 可批次刪除指定資料夾下所有指定副檔名的檔案"""
    # 準備資料夾與多個 .json 檔
    test_dir = tmp_path / "to_clear"
    ensure_dir(test_dir)
    files = [test_dir / f"test{i}.json" for i in range(5)]
    for f in files:
        f.write_text("dummy", encoding="utf-8")
    # 再加一個 .txt 檔案，不應被刪除
    txt_file = test_dir / "not_json.txt"
    txt_file.write_text("should remain", encoding="utf-8")

    from utils.file.file_helper import clear_dir_files

    # 呼叫清理工具
    count = clear_dir_files(test_dir)
    assert count == 5
    # 檢查所有 .json 都被刪除，.txt 檔案仍在
    assert all(not f.exists() for f in files)
    assert txt_file.exists()
