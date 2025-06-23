from datetime import datetime
from pathlib import Path
from workspace.config.paths import get_report_dir
from workspace.config.rules.error_codes import ResultCode
from workspace.utils.file.file_helper import ensure_dir, delete_file

def prepare_report_directory(phase: str) -> Path:
    """
    確保該測試階段的報告資料夾存在，並刪除舊的 HTML 報告。
    :param phase: 測試階段名稱，例如 'unit'
    :return: 清理完成的 phase 子資料夾路徑
    """
    report_dir = get_report_dir() / phase

    # 確保子資料夾存在
    result = ensure_dir(report_dir)
    if result != ResultCode.SUCCESS:
        raise RuntimeError(f"建立報告資料夾失敗: {report_dir}")

    # 刪除舊報告
    for html_file in report_dir.glob("*.html"):
        delete_result = delete_file(html_file)
        if delete_result != ResultCode.SUCCESS:
            print(f"[WARN] 無法刪除舊報告: {html_file}")

    return report_dir


def get_timestamped_report_path(phase: str) -> Path:
    """
    產生帶有時間戳的 pytest-html 報告檔案路徑
    :param phase: 測試階段名稱
    :return: 含完整檔案名稱的 Path
    """
    report_dir = prepare_report_directory(phase)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    filename = f"{phase}_test_report_{timestamp}.html"
    return report_dir / filename
