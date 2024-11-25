@echo off
chcp 65001 >nul
echo Скачивание файла...
curl -s -L https://ekoeden.space/subvpn/c0sxnocxy3ijorra > configs\profile.json
if %errorlevel% neq 0 (
    echo Ошибка при обновлении.
    pause
    exit\b
)
echo Файл успешно обновлен.
sub_converter.exe
