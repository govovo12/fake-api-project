@echo off
echo [SYNC] Resetting local branch to match remote...

:: 切回專案根目錄（bat 上層）
cd /d "%~dp0.."

:: Get current branch name
for /f %%i in ('git branch --show-current') do set CUR_BRANCH=%%i

:: Reset to remote branch
git fetch origin
git reset --hard origin/%CUR_BRANCH%
git clean -fdx

:: Extra: try removing common venv folders
if exist venv (
    echo [CLEAN] Deleting venv folder...
    rmdir /s /q venv
)

if exist .venv (
    echo [CLEAN] Deleting .venv folder...
    rmdir /s /q .venv
)

echo [DONE] Local project is now reset to origin/%CUR_BRANCH%
pause
