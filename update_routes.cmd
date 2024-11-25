@echo off
cd /d "%~dp0bin"
call routes.cmd

:: Проверяем статус службы WinSW
for /f "tokens=*" %%a in ('WinSW.exe status') do set status=%%a
if "%status%"=="Started" (
    WinSW.exe restart
)

pause