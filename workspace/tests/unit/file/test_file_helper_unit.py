import pytest
import json
from pathlib import Path
from workspace.utils.file.file_helper import (
    ensure_dir,
    ensure_file,
    file_exists,
    is_file_empty,
    get_file_name_from_path,
    clear_file,
    save_json,
    generate_testdata_path
)

pytestmark = [pytest.mark.unit, pytest.mark.file]

@pytest.fixture
def temp_dir(tmp_path) -> Path:
    return tmp_path / "test_dir"


def test_ensure_dir_creates_directory(temp_dir):
    assert not temp_dir.exists()
    ensure_dir(temp_dir)
    assert temp_dir.exists()
    assert temp_dir.is_dir()


def test_ensure_file_creates_file(tmp_path):
    file_path = tmp_path / "empty.json"
    assert not file_path.exists()
    ensure_file(file_path)
    assert file_path.exists()
    assert file_path.read_text() == ""


def test_file_exists_returns_true(tmp_path):
    file_path = tmp_path / "exists.json"
    file_path.write_text("content")
    assert file_exists(file_path)


def test_file_exists_returns_false(tmp_path):
    file_path = tmp_path / "not_exist.json"
    assert not file_exists(file_path)


def test_is_file_empty_true(tmp_path):
    file_path = tmp_path / "empty.json"
    file_path.write_text("")
    assert is_file_empty(file_path)


def test_is_file_empty_false(tmp_path):
    file_path = tmp_path / "not_empty.json"
    file_path.write_text("data")
    assert not is_file_empty(file_path)


def test_get_file_name_from_path():
    path = Path("some/folder/data.json")
    assert get_file_name_from_path(path) == "data.json"


def test_clear_file_empties_file(tmp_path):
    file_path = tmp_path / "to_clear.json"
    file_path.write_text("some data")
    clear_file(file_path)
    assert file_path.exists()
    assert file_path.read_text() == ""


def test_save_json_success(tmp_path):
    file_path = tmp_path / "data.json"
    success, meta = save_json(file_path, {"a": 1, "b": 2})
    assert success is True
    assert meta is None
    content = json.loads(file_path.read_text())
    assert content == {"a": 1, "b": 2}


def test_save_json_serialization_fail(tmp_path):
    file_path = tmp_path / "fail.json"
    success, meta = save_json(file_path, {"bad": set()})
    assert not success
    assert meta["reason"] == "json_serialization_failed"
    assert "fail.json" in meta["path"]


def test_generate_testdata_path_valid():
    path, meta = generate_testdata_path("user", "a" * 32)
    assert path is not None
    assert meta is None
    assert path.name.endswith(".json")


def test_generate_testdata_path_invalid_kind():
    path, meta = generate_testdata_path("order", "a" * 32)
    assert path is None
    assert meta["reason"] == "invalid_kind"


def test_generate_testdata_path_invalid_uuid():
    path, meta = generate_testdata_path("user", "123")
    assert path is None
    assert meta["reason"] == "invalid_uuid"
