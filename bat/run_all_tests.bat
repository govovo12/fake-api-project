@echo off
chcp 65001 > nul
cd /d "%~dp0.."
python workspace/utils/run_launcher.py
pause
