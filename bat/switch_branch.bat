@echo off
chcp 65001 > nul
title 🔁 Git 分支切換工具

:: 切到專案目錄
cd /d C:\Users\user\Desktop\fake-api-project

:: 顯示目前所在分支
echo.
echo === 目前分支列表 ===
git branch

:: 讓使用者輸入欲切換分支名稱
echo.
set /p BRANCH=請輸入要切換的分支名稱（例如：dev 或 main）： 

:: 嘗試切換分支
echo.
echo 正在切換到分支：%BRANCH%
git checkout %BRANCH%

:: 顯示切換後狀態
echo.
echo ✅ 切換後的狀態：
git status

echo.
pause
