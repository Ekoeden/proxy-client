@echo off
cd /d "%~dp0bin"
chcp 65001 >nul

:: Admin rights check
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Скрипт запущен без прав администратора.
    echo Перезапустите с правами администратора.
    pause
    exit /b
)

call profile_input.cmd

:: WinSW service check
set "status="
for /f "tokens=* delims=" %%a in ('WinSW.exe status') do set "status=%%a"

:: Remove spaces on the sides, if any
set "status=%status: =%"

if "%status%" neq "NonExistent" (
    if "%status%"=="Started" (
        WinSW.exe stop
    )
    WinSW.exe uninstall
)

call routes.cmd routes
WinSW.exe install
WinSW.exe start
pause