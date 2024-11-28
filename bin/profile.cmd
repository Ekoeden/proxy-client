@echo off
chcp 65001 >nul
echo Скачивание файла...
curl -s -L ~URL~ > configs\profile.json
if %errorlevel% neq 0 (
    echo Ошибка при обновлении.
    pause
    exit\b
)
echo Файл успешно обновлен.
sub_converter.exe
