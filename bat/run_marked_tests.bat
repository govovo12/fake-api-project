@echo off
cd /d %~dp0..
call venv\Scripts\activate
for /f "delims=" %%i in ('python workspace\print_all_marks.py') do set CMD=%%i
echo Running: %CMD%
%CMD%
pause
