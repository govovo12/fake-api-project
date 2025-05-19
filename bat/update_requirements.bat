@echo off
:: Switch to project root (parent of this .bat)
cd /d "%~dp0.."

echo [INFO] Checking installed packages...
pip freeze > .current_freeze.txt

if not exist requirements.txt (
    echo [INFO] No requirements.txt found, creating an empty one...
    echo. > requirements.txt
)

echo [INFO] Merging package list with requirements.txt...
type requirements.txt .current_freeze.txt > .combined.txt

echo import sys > .merge_script.py
echo lines = set(open(".combined.txt").readlines()) >> .merge_script.py
echo open("requirements.txt", "w").writelines(sorted(lines)) >> .merge_script.py
python .merge_script.py

del .current_freeze.txt
del .combined.txt
del .merge_script.py

echo [SUCCESS] requirements.txt has been updated.
pause

