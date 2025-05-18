@echo off
cd /d %~dp0
echo 正在列出專案結構...
python print_clean_structure.py
pause
