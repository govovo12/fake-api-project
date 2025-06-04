@echo off

REM Move to the directory of this .bat file
cd /d %~dp0
cd ..

REM Show current directory (for debugging)
echo Current working directory:
cd

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found in .venv\
    pause
    exit /b
)

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Run pytest
call .venv\Scripts\python.exe -m pytest workspace/tests

REM Pause the terminal window
pause
