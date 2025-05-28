@echo off
echo === Cleaning Python __pycache__ and .pyc files ===

for /r %%i in (__pycache__) do (
    if exist "%%i" (
        echo Deleting: %%i
        rmdir /s /q "%%i"
    )
)

for /r %%i in (*.pyc) do (
    echo Deleting: %%i
    del /f /q "%%i"
)

echo === Done. All caches cleared. ===
pause
