@echo off
REM 切換到 workspace/scripts 目錄
cd /d %~dp0..\workspace\scripts

REM 啟動虛擬環境 (視你虛擬環境路徑調整)
call ..\..\venv\Scripts\activate.bat

REM 執行 gen_tools_table.py
python gen_tools_table.py

pause
