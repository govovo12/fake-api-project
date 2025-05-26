@echo off
cd /d %~dp0..

call venv\Scripts\activate

set PYTHONPATH=workspace

pytest workspace/tests --tb=short -s --html=workspace/reports/account_generator_report.html --self-contained-html

pause
