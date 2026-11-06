@echo off
chcp 936 >nul
if "%~1"=="" (
  echo 用法: 推送到GitHub.bat https://github.com/你的用户名/仓库名.git
  echo.
  echo 请先在 GitHub 新建一个空仓库，不要勾选初始化 README / .gitignore / License。
  pause
  exit /b 1
)
cd /d "%~dp0"
echo 目标仓库: %~1
echo.
git remote remove origin >nul 2>&1
git remote add origin "%~1"
git push -u origin main
if errorlevel 1 (
  echo.
  echo 推送失败，请检查仓库地址、网络，或确认该仓库是空的。
) else (
  echo.
  echo 推送完成，打开 GitHub 仓库页面刷新即可看到源码。
)
pause
