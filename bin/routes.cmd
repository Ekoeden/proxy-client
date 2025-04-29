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
curl --fail -s -L -o temp_response.json !baseLink!!fileName!.json

:: Проверка успешности загрузки
if errorlevel 1 (
    echo Файл !fileName! не найден. Пожалуйста, попробуйте снова.
    del temp_response.json 2>nul
    pause
    cls
    goto start
)

:: Проверка, является ли ответ страницей ошибки
findstr /i "<html" temp_response.json >nul 2>&1
if %errorlevel%==0 (
    echo Файл !fileName! не найден. Пожалуйста, попробуйте снова.
    del temp_response.json
    pause
    cls
    goto start
)

echo Файл найден. Скачивание файла...
move /Y temp_response.json configs\routes.json >nul

:: Проверка успешности перемещения
if errorlevel 1 (
    echo Ошибка при обновлении файла.
    del temp_response.json 2>nul
) else (
    echo Файл успешно обновлен.
)

exit /b