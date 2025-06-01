import pytest
from pathlib import Path

pytestmark = [pytest.mark.unit, pytest.mark.fixture]

def tool(func):
    func.is_tool = True
    return func

@pytest.fixture
@tool
def temp_file(tmp_path: Path):
    """產生一個臨時檔案，for 檔案測試 [TOOL]"""
    file_path = tmp_path / "test.txt"
    file_path.write_text("stub file content", encoding="utf-8")
    return file_path
