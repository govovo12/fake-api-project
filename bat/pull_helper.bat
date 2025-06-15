@echo off
echo [SYNC] Resetting local branch to match remote...

:: Get current branch name
for /f %%i in ('git branch --show-current') do set CUR_BRANCH=%%i

:: Reset to remote branch
git fetch origin
git reset --hard origin/%CUR_BRANCH%

:: Clean all untracked files including those in .gitignore
git clean -fdx

:: Extra: Force remove venv folder if exists
if exist venv (
    echo [CLEAN] Deleting local venv folder...
    rmdir /s /q venv
)

echo [DONE] Local project is now reset to origin/%CUR_BRANCH%
pause
