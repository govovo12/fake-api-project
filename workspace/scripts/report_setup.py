"""
📦 報告路徑與覆蓋率工具模組
"""

from pathlib import Path
from datetime import datetime
from coverage import Coverage
import shutil
from workspace.config.paths import (
    get_report_dir,
    get_phase_report_dir,
    get_phase_coverage_dir,
    get_htmlcov_dir,
)


def get_timestamped_report_path(phase: str) -> Path:
    """產生加時間戳的測試報告路徑"""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    filename = f"{phase}_test_report_{timestamp}.html"
    return get_phase_report_dir(phase) / filename


def get_coverage_output_path(phase: str) -> Path:
    """取得各階段 coverage 輸出目錄"""
    return get_phase_coverage_dir(phase)


def reset_report_root():
    """重置 reports 根目錄（包含 coverage/total）"""
    report_root = get_report_dir()
    if report_root.exists():
        for sub in report_root.iterdir():
            if sub.is_file():
                sub.unlink()
            else:
                shutil.rmtree(sub)
    report_root.mkdir(parents=True, exist_ok=True)




def combine_coverage_reports():
    """🧪 將所有階段 coverage 資料合併為 reports/coverage/total"""
    coverage_dir = get_report_dir() / "coverage"
    htmlcov_total_dir = coverage_dir / "total"
    htmlcov_total_dir.mkdir(parents=True, exist_ok=True)

    cov_files = list(coverage_dir.glob(".coverage.*"))
    if not cov_files:
        print("⚠️ 找不到可合併的 coverage 檔案")
        return

    cov = Coverage(
        data_file=str(htmlcov_total_dir / ".coverage"),
        source=["workspace"],  # ⬅️ 加這行讓未執行的模組也統計進去
    )
    cov.combine([str(f) for f in cov_files])
    cov.save()
    cov.html_report(directory=str(htmlcov_total_dir), include="workspace/*")




def generate_index_html(report_root: Path = None) -> None:
    """產出總覽 index.html，包含各測試報告與各階段 coverage 連結"""
    if report_root is None:
        report_root = get_report_dir()

    index_file = report_root / "index.html"
    content = ["<html><head><meta charset='utf-8'><title>測試報告總覽</title></head><body>"]
    content.append("<h1>測試報告總覽</h1><ul>")

    for phase in ["unit", "infra", "integration", "e2e"]:
        phase_dir = get_phase_report_dir(phase)
        coverage_dir = get_phase_coverage_dir(phase)

        # 測試報告連結
        report_files = sorted(phase_dir.glob("*.html"), reverse=True)
        if report_files:
            latest_report = report_files[0].name
            content.append(f"<li><a href='{phase}/{latest_report}'>{phase} 測試報告</a></li>")

        # 覆蓋率報告連結
        if (coverage_dir / "index.html").exists():
            content.append(f"<li><a href='coverage/{phase}/index.html'>{phase} 覆蓋率報告</a></li>")

    # 🌟 總體覆蓋率
    total_dir = get_report_dir() / "coverage" / "total"
    if (total_dir / "index.html").exists():
        content.append("<li><a href='coverage/total/index.html'>🌟 總體覆蓋率報告</a></li>")

    content.append("</ul></body></html>")
    index_file.write_text("\n".join(content), encoding="utf-8")
