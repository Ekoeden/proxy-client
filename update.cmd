@echo off
cd /d "%~dp0bin"

timeout /t 2 >nul
move /y "update.exe" "new_update.exe"
"new_update.exe"
del "new_update.exe"

:: Проверяем статус службы WinSW
for /f "tokens=*" %%a in ('WinSW.exe status') do set status=%%a
if "%status%"=="Started" (
    WinSW.exe restart
)

pause