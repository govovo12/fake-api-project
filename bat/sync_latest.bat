@echo off
cd /d C:\Users\user\Desktop\fake-api-project

REM 拉遠端並強制同步
git fetch origin
git clean -fd
git reset --hard origin/main

echo ✅ 已強制覆蓋拉取最新版本！
pause
