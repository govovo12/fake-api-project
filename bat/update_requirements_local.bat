@echo off
cd /d C:\Users\user\Desktop\fake-api-project

echo [INFO] Using pip from venv\Scripts\pip.exe
venv\Scripts\pip.exe -V
venv\Scripts\pip.exe freeze > requirements.txt

echo [SUCCESS] requirements.txt has been updated.
echo [PREVIEW]
type requirements.txt
pause
