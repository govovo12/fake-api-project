@echo off
cd /d %~dp0
echo 正在顯示專案結構...
python ..\workspace\print_clean_structure.py
pause
