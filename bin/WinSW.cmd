cd /d "%~dp0"
copy /y NUL WinSW.wrapper.log
sing-box.exe run -C configs
