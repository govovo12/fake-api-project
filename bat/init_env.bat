@echo off
cd /d %~dp0\..
setlocal

REM === 安全檢查 ===
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt 不存在，請確認您是否在正確的專案目錄中執行。
    pause
    exit /b
)

echo [INFO] 建立虛擬環境 venv...
python -m venv venv

echo [INFO] 安裝 requirements.txt 中的套件...
venv\Scripts\pip.exe install -r requirements.txt

echo [SUCCESS] 環境初始化完成！
pause
