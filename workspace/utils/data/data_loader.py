# utils/data/data_loader.py
import json
from pathlib import Path
from controller import log_controller


def load_json(path: Path) -> dict:
    """
    安全載入 JSON 檔案，失敗時回傳空 dict 並記錄錯誤。
    """
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log_controller.error(f"JSON讀取失敗：{path.name}", code="JSON_LOAD_FAIL")
        return {}


def load_json_by_name(filename: str, subdir: str = "") -> dict:
    from utils import paths
    target_path = paths.TESTDATA_PATH / subdir / filename if subdir else paths.TESTDATA_PATH / filename
    return load_json(target_path)
