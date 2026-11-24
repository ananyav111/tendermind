@echo off
setlocal

echo ========================================================
echo   TenderMind - Push to GitHub Automation
echo ========================================================
echo.

set /p REPO_URL="Enter your GitHub repository URL (press Enter to keep existing origin): "

if not "%REPO_URL%"=="" (
    echo [1/3] Configuring Git remote origin to %REPO_URL%...
    git remote remove origin 2>nul
    git remote add origin %REPO_URL%
) else (
    echo [1/3] Using existing configured remote origin...
)

echo [2/3] Setting branch to main...
git branch -M main

echo [3/3] Pushing commits to GitHub...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo   SUCCESS! Project successfully pushed to GitHub!
    echo ========================================================
) else (
    echo.
    echo [ERROR] Git push failed. Please check your repository URL and credentials.
)

pause
