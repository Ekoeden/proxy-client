@echo off
cd /d "%~dp0bin"

timeout /t 2 >nul
move /y "update.exe" "new_update.exe" >nul

:: Проверяем статус службы WinSW
for /f "tokens=*" %%a in ('WinSW.exe status') do set status=%%a
if "%status%"=="Started" (
    WinSW.exe stop
    "new_update.exe"
    WinSW.exe start
) else (
    "new_update.exe"
)

del "new_update.exe"
pause
