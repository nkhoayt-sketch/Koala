@echo off
title JLPT N1 Quiz Web Server
cd /d "%~dp0"
echo ========================================================
echo   Khoi dong Web App Luyen thi N1 (20 ngay)
echo   Dang khoi chay may chu cuc bo...
echo ========================================================
powershell -ExecutionPolicy Bypass -File "%~dp0server.ps1"
pause
