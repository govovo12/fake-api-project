import pytest
from pathlib import Path
from workspace.utils.file import file_helper
from workspace.config.rules.error_codes import ResultCode
from workspace.utils.file.file_helper import TaskModuleError

# ✅ 測試標記：單元測試 + file 分類
pytestmark = [pytest.mark.unit, pytest.mark.file]

def test_ensure_dir(tmp_path):
    test_dir = tmp_path / "testdir"
    file_helper.ensure_dir(test_dir)
    assert test_dir.exists() and test_dir.is_dir()


def test_ensure_file(tmp_path):
    test_file = tmp_path / "f.txt"
    file_helper.ensure_file(test_file)
    assert test_file.exists() and test_file.is_file()


def test_file_exists_true(tmp_path):
    f = tmp_path / "exist.txt"
    f.write_text("123")
    assert file_helper.file_exists(f) is True


def test_file_exists_false(tmp_path):
    f = tmp_path / "nonexist.txt"
    assert file_helper.file_exists(f) is False


def test_is_file_empty_true(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_text("")
    assert file_helper.is_file_empty(f) is True


def test_is_file_empty_false(tmp_path):
    f = tmp_path / "notempty.txt"
    f.write_text("hello")
    assert file_helper.is_file_empty(f) is False


def test_get_file_name_from_path():
    path = Path("a/b/c/file.json")
    assert file_helper.get_file_name_from_path(path) == "file.json"


def test_clear_file(tmp_path):
    f = tmp_path / "to_clear.txt"
    f.write_text("some content")
    file_helper.clear_file(f)
    assert f.read_text() == ""


def test_save_json_success(tmp_path):
    f = tmp_path / "data.json"
    data = {"k": 1}
    file_helper.save_json(f, data)
    assert f.exists()
    assert f.read_text().strip().startswith("{")


def test_save_json_type_error(tmp_path):
    f = tmp_path / "bad.json"

    class BadType:
        pass

    with pytest.raises(TaskModuleError) as e:
        file_helper.save_json(f, {"x": BadType()})
    assert e.value.code == ResultCode.FILE_SERIALIZATION_FAILED


def test_generate_testdata_path_success():
    path = file_helper.generate_testdata_path("user", "1234567890abcdef1234567890abcdef")
    assert isinstance(path, Path)
    assert "user" in str(path)


def test_generate_testdata_path_invalid_kind():
    with pytest.raises(TaskModuleError) as e:
        file_helper.generate_testdata_path("invalid", "1234567890abcdef1234567890abcdef")
    assert e.value.code == ResultCode.INVALID_FILE_KIND


def test_generate_testdata_path_invalid_uuid():
    with pytest.raises(TaskModuleError) as e:
        file_helper.generate_testdata_path("user", "short-id")
    assert e.value.code == ResultCode.UUID_FORMAT_INVALID


def test_write_temp_file_success():
    p = file_helper.write_temp_file("hello")
    assert p.exists()
    assert p.read_text() == "hello"
