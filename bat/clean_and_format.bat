@echo off
REM Activate the virtual environment
call ..\venv\Scripts\activate.bat

echo === Exporting requirements.txt ===
pip freeze > requirements.txt
if errorlevel 1 (
    echo Failed to export requirements.txt
) else (
    echo requirements.txt updated successfully.
)

echo.
echo === Cleaning __pycache__ folders ===
for /d /r %%i in (__pycache__) do (
    if exist "%%i" (
        rd /s /q "%%i"
        echo Removed %%i
    )
)
echo __pycache__ cleanup completed.

echo.
echo === Formatting code with Black & isort ===
black .
if errorlevel 1 (
    echo Black formatting failed.
) else (
    echo Black formatting completed.
)
isort .
if errorlevel 1 (
    echo isort formatting failed.
) else (
    echo isort formatting completed.
)

pause
