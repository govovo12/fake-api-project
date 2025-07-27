@echo off
REM ========================================
REM ✅ 執行完整測試流程（本地 CLI）
REM 使用方式：直接雙擊或命令列執行此檔
REM ========================================

REM ✅ 切換到專案根目錄
cd /d %~dp0
cd ..

REM ✅ 啟動虛擬環境（若存在）
if exist venv\Scripts\activate (
    call venv\Scripts\activate
)

REM ✅ 執行測試總流程
python workspace/scripts/run_test_pipeline.py

pause
