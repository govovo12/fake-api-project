@echo off
chcp 65001 > nul
cd /d C:\Users\user\Desktop\fake-api-project

echo 🔄 Starting sync with remote...

git fetch origin
git clean -fd
git reset --hard origin/main

echo ✅ Sync complete - local is now at origin/main
pause
