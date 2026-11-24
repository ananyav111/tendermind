@echo off
setlocal

echo ========================================================
echo   TenderMind - Push to GitHub Automation
echo ========================================================
echo.

set /p REPO_URL="Enter your GitHub repository URL (e.g. https://github.com/username/tendermind.git): "

if "%REPO_URL%"=="" (
    echo [ERROR] Repository URL cannot be empty.
    pause
    exit /b 1
)

echo.
echo [1/3] Configuring Git remote origin...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo [2/3] Setting branch to main...
git branch -M main

echo [3/3] Pushing commits to GitHub...
git push -u origin %REPO_URL% main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo   SUCCESS! Project successfully pushed to:
    echo   %REPO_URL%
    echo ========================================================
) else (
    echo.
    echo [ERROR] Git push failed. Please check your repository URL and credentials.
)

pause
