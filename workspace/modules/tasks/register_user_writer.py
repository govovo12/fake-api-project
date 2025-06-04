from pathlib import Path
from workspace.utils.file.file_helper import ensure_file
from workspace.utils.data.data_loader import load_json, save_json

def write_user_to_json(user: dict, file_path: Path) -> dict:
    """
    將單筆 user 資料（含 uuid）寫入指定 JSON 檔案中，採 append 模式。

    Args:
        user (dict): 欲寫入的使用者資料，需由控制器加上 uuid 欄位。
        file_path (Path): JSON 檔案完整路徑

    Returns:
        dict: 實際寫入的 user 資料（含 uuid）
    """
    ensure_file(file_path)

    data = load_json(file_path)
    if not isinstance(data, list):
        data = []

    data.append(user)
    save_json(data, file_path)
    return user
