@echo off
setlocal
set "PATH=C:\Program Files\Git\cmd;%PATH%"
cd /d "%~dp0"
echo =========================================================
echo   PUSHING KOALA JLPT HUB TO GITHUB REPOSITORY...
echo   Target: https://github.com/nkhoayt-sketch/Koala.git
echo =========================================================
echo.
git push -u origin main
echo.
if %errorlevel% equ 0 (
    echo =========================================================
    echo   [SUCCESS] PUSH COMPLETED SUCCESSFULLY!
    echo   View repo: https://github.com/nkhoayt-sketch/Koala
    echo =========================================================
) else (
    echo [ERROR] Push failed. Please check your GitHub credentials.
)
echo.
pause
