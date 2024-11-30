@echo off
cd /d "%~dp0bin"
chcp 65001 >nul

:: Проверяем статус службы WinSW
for /f "tokens=*" %%a in ('WinSW.exe status') do set status=%%a
if "%status%"=="Started" (
    WinSW.exe stop
    update.exe
    WinSW.exe start
) else (
    update.exe
)

pause
