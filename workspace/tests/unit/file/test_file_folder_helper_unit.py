import pytest
from pathlib import Path
from workspace.utils.file import file_helper, folder_helper
import os

@pytest.mark.file
def test_write_temp_file_and_file_exists():
    path = file_helper.write_temp_file("hello", suffix=".log")
    assert file_helper.file_exists(path)
    assert path.suffix == ".log"
    path.unlink()

@pytest.mark.file
def test_file_exists_false():
    path = Path("nonexistent_file_123.txt")
    assert not file_helper.file_exists(path)

@pytest.mark.file
def test_ensure_dir(tmp_path):
    test_dir = tmp_path / "a" / "b"
    assert not test_dir.exists()
    folder_helper.ensure_dir(test_dir)
    assert test_dir.exists()

@pytest.mark.file
def test_clear_folder(tmp_path):
    folder = tmp_path / "data"
    folder.mkdir()
    (folder / "x.txt").write_text("x")
    (folder / "y.txt").write_text("y")
    folder_helper.clear_folder(folder)
    assert not any(folder.iterdir())
