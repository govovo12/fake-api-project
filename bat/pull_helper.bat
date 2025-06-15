@echo off
echo 🔄 Starting reset to latest remote state...

:: 取得當前分支
for /f %%i in ('git branch --show-current') do set CUR_BRANCH=%%i

:: 拉最新 + 強制重設
git fetch origin
git reset --hard origin/%CUR_BRANCH%

:: 刪除未追蹤的檔案與資料夾（包括 venv）
git clean -fd

echo ✅ Reset complete - project is now synced with origin/%CUR_BRANCH%
pause
