import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from scripts import report_setup


pytestmark = [pytest.mark.unit, pytest.mark.report]


def test_get_timestamped_report_path():
    """✅ 測試報告檔案產生有時間戳與對應 phase"""
    path = report_setup.get_timestamped_report_path("unit")
    assert "unit_test_report_" in path.name
    assert path.suffix == ".html"


def test_prepare_report_directory_creates_dir(tmp_path, monkeypatch):
    """✅ 確保能建立 reports 根目錄"""
    monkeypatch.setattr(report_setup, "get_report_dir", lambda: tmp_path / "reports")
    report_setup.reset_report_root()
    assert (tmp_path / "reports").exists()


def test_prepare_report_directory_clears_old_data(tmp_path, monkeypatch):
    """✅ 確保能清除原本的測試資料"""
    root = tmp_path / "reports"
    dummy_file = root / "old.txt"
    root.mkdir()
    dummy_file.write_text("hello")

    monkeypatch.setattr(report_setup, "get_report_dir", lambda: root)
    report_setup.reset_report_root()

    assert not dummy_file.exists()
    assert root.exists() and list(root.iterdir()) == []


def test_get_coverage_output_path():
    """✅ 測試覆蓋率資料夾路徑取得"""
    path = report_setup.get_coverage_output_path("unit")
    assert "unit" in str(path)


def test_combine_coverage_reports_creates_total_html(tmp_path, monkeypatch):
    """✅ 測試 combine_coverage_reports 可正常建立 reports/coverage/total/index.html"""

    # 模擬 coverage 檔案們
    coverage_dir = tmp_path / "reports" / "coverage"
    coverage_dir.mkdir(parents=True)

    for name in [".coverage.unit", ".coverage.infra", ".coverage.integration", ".coverage.e2e"]:
        (coverage_dir / name).write_text("fake")

    total_cov_dir = coverage_dir / "total"

    # patch get_report_dir()
    monkeypatch.setattr(report_setup, "get_report_dir", lambda: tmp_path / "reports")

    # 模擬 Coverage 行為
    fake_cov = MagicMock()
    with patch("scripts.report_setup.Coverage", return_value=fake_cov) as mock_coverage:
        report_setup.combine_coverage_reports()

        mock_coverage.assert_called_once()
        fake_cov.combine.assert_called_once()
        fake_cov.html_report.assert_called_once_with(
            directory=str(total_cov_dir),
            include="workspace/*",
        )



def test_generate_index_html(tmp_path, monkeypatch):
    """✅ 測試 index.html 能產出所有連結"""
    reports_dir = tmp_path / "reports"
    (reports_dir / "unit").mkdir(parents=True)
    (reports_dir / "unit" / "sample.html").write_text("test")

    (reports_dir / "coverage" / "unit").mkdir(parents=True)
    (reports_dir / "coverage" / "unit" / "index.html").write_text("cov")

    (reports_dir / "coverage" / "total").mkdir(parents=True)
    (reports_dir / "coverage" / "total" / "index.html").write_text("total cov")

    monkeypatch.setattr(report_setup, "get_report_dir", lambda: reports_dir)
    monkeypatch.setattr(report_setup, "get_phase_report_dir", lambda phase: reports_dir / phase)
    monkeypatch.setattr(report_setup, "get_phase_coverage_dir", lambda phase: reports_dir / "coverage" / phase)

    report_setup.generate_index_html()

    index_file = reports_dir / "index.html"
    assert index_file.exists()
    content = index_file.read_text(encoding="utf-8")
    assert "unit/sample.html" in content
    assert "coverage/unit/index.html" in content
    assert "coverage/total/index.html" in content
