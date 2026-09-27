@echo off
chcp 65001 > nul
title Đẩy mã nguồn Koala JLPT Hub lên GitHub
echo =================================================================
echo   ĐANG ĐẨY TOÀN BỘ MÃ NGUỒN KOALA LÊN GITHUB REPOSITORY...
echo   Repository: https://github.com/nkhoayt-sketch/Koala.git
echo =================================================================
echo.

"C:\Program Files\Git\cmd\git.exe" push -u origin main

echo.
if %errorlevel% equ 0 (
    echo =================================================================
    echo   [THÀNH CÔNG] Đã đẩy toàn bộ mã nguồn lên GitHub hoàn tất!
    echo   Xem tại: https://github.com/nkhoayt-sketch/Koala
    echo =================================================================
) else (
    echo [LỖI] Quá trình push gặp sự cố. Vui lòng kiểm tra quyền đăng nhập GitHub.
)
echo.
pause
