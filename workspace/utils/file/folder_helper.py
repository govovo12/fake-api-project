from pathlib import Path

def ensure_dir(path: Path):
    """確保資料夾存在，若無則遞迴建立"""
    path.mkdir(parents=True, exist_ok=True)

def clear_folder(path: Path):
    """清空指定資料夾下所有檔案"""
    if not path.exists():
        return
    for file in path.iterdir():
        if file.is_file():
            file.unlink()
