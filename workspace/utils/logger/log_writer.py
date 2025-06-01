from pathlib import Path

def tool(func):
    """自製工具標記（供自動掃描工具表用）"""
    func.is_tool = True
    return func

@tool
def write_log(log_path: Path, message: str) -> None:
    """
    [TOOL] 寫入 log 訊息到指定檔案。
    - 不會檢查資料夾/檔案是否存在
    - 不處理時間戳記（需外層組合）
    """
    with log_path.open(mode="a", encoding="utf-8") as f:
        f.write(f"{message}\n")
