@echo off
REM 切換到專案根目錄
cd /d %~dp0..

REM 啟動虛擬環境
call venv\Scripts\activate.bat

REM 執行 pytest
pytest

pause
