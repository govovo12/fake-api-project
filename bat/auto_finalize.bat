@echo off
cd /d C:\Users\user\Desktop\fake-api-project

REM 啟用虛擬環境
call venv\Scripts\activate.bat

REM 匯出目前虛擬環境套件列表
pip freeze > requirements.txt

REM 執行專案根目錄的 Python 工具腳本
python finalize_helper.py

pause
