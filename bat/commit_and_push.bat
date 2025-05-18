@echo off
chcp 65001 > nul
title 🚀 Git 一鍵 Commit & Push 工具

:: 切換到你的專案目錄
cd /d C:\Users\user\Desktop\fake-api-project

:: 顯示目前所在分支
for /f "delims=" %%b in ('git branch --show-current') do set BRANCH=%%b

:: 顯示 Git 狀態
echo.
echo 🔍 當前分支：%BRANCH%
git status

:: 等待使用者輸入 commit 訊息
echo.
set /p MSG=請輸入 commit 訊息（如：Fix login bug）： 

:: 加入所有異動（新增 + 修改 + 刪除）
git add -A

:: 提交
git commit -m "%MSG%"

:: 推送
git push origin %BRANCH%

echo.
echo ✅ 已成功提交並推送至分支 %BRANCH%
pause
