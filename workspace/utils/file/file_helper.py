from pathlib import Path
from tempfile import NamedTemporaryFile

def write_temp_file(content: str, suffix: str = ".txt") -> Path:
    """寫入暫存檔案，回傳檔案路徑"""
    with NamedTemporaryFile(delete=False, mode="w", suffix=suffix, encoding="utf-8") as f:
        f.write(content)
        return Path(f.name)

def file_exists(path: Path) -> bool:
    """檢查檔案是否存在"""
    return path.is_file()
