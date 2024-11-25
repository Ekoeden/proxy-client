@echo off
cd /d "%~dp0bin"

:: Проверяем статус службы WinSW
for /f "tokens=*" %%a in ('WinSW.exe status') do set status=%%a
if "%status%"=="Started" (
    WinSW.exe stop
    WinSW.exe uninstall
) else (
    WinSW.exe uninstall
)

pause