from pathlib import Path
import json
from typing import Any

def tool(func):
    """自製工具標記，供自動產生工具表用"""
    func.is_tool = True
    return func

@tool
def export_json(data: Any, path: Path):
    """
    將任意資料寫入 JSON 檔案，自動建立上層資料夾 [TOOL]
    - data: 任意可序列化資料
    - path: 輸出 JSON 檔案路徑（支援自動建立目錄）
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@tool
def export_text(content: str, path: Path):
    """
    將文字寫入純文字檔案，支援自動建立資料夾 [TOOL]
    - content: 輸出內容字串
    - path: 輸出檔案路徑（支援自動建立目錄）
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
