@echo off
cd /d "%~dp0bin"
python update.py

:: Проверяем статус службы WinSW
for /f "tokens=*" %%a in ('WinSW.exe status') do set status=%%a
if "%status%"=="Started" (
    WinSW.exe restart
)

pause