@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Ссылка на репозиторий
set "baseLink=https://raw.githubusercontent.com/Ekoeden/proxy-client/routes/"

:: Проверка наличия аргумента
:start
if "%~1"=="" (
    set /p "fileName=Введите название набора маршрутов: "
) else (
    set "fileName=%~1"
)

:: Проверка наличия файла
echo Проверка наличия файла маршрутов...
curl -s -L -o temp_response.html -H "Accept: application/vnd.github+json" -H "Authorization: token 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" !baseLink!!fileName!.json

:: Проверка, является ли ответ страницей ошибки
findstr /i "html" temp_response.html >nul
if %errorlevel%==0 (
    echo Файл !fileName! не найден. Пожалуйста, попробуйте снова.
    del temp_response.html
    pause
    cls
    goto start
)

echo Файл найден. Скачивание файла...
move /Y temp_response.html configs\routes.json >nul
echo Файл успешно обновлен.

exit /b