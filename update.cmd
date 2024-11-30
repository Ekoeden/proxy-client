@echo off
cd /d "%~dp0bin"

for /f "tokens=*" %%a in ('WinSW.exe status') do set status=%%a
if "%status%"=="Started" (
    WinSW.exe stop
)

copy /y "update.exe" "new_update.exe" >nul
"new_update.exe"
del "new_update.exe"

if "%status%"=="Started" (
    WinSW.exe start
)

pause
