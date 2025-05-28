from pathlib import Path
import json
from typing import Any

def export_json(data: Any, path: Path):
    """將任意資料寫入 JSON 檔案，自動建立上層資料夾"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def export_text(content: str, path: Path):
    """將文字寫入純文字檔案，支援自動建立資料夾"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
