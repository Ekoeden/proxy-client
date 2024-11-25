@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Запрос URL у пользователя
:start
set /p "new_url=Введите ссылку на ваш профиль vless: "

:: :::::
echo Проверка наличия файла профиля...
curl -s -L --fail %new_url% -o configs\profile.json

:: Проверка на ошибку загрузки через код возврата curl
if %errorlevel% neq 0 (
    echo Ошибка: Проверьте ссылку и подключение.
    del configs\profile.json
    pause
    cls
    goto start
)

:: Проверка на наличие строки с base64 префиксом "dmxlc3M6Ly" (vless:/)
findstr /b /c:"dmxlc3M6Ly" configs\profile.json >nul
if %errorlevel% neq 0 (
    echo Ошибка: Файл не содержит корректные данные.
    del configs\profile.json
    pause
    cls
    goto start
)

echo Файл найден. Скачивание файла...
:: :::::

:: Путь к файлу, который нужно изменить
set "file_path=profile.cmd"

:: Временный файл для записи изменений
set "temp_file=%file_path%.tmp"

:: Чтение файла построчно и замена URL
> "%temp_file%" (
    for /f "usebackq delims=" %%i in ("%file_path%") do (
        set "line=%%i"
        
        if not "!line!"=="!line:curl -s -L =!" (
            set "line=curl -s -L %new_url% > configs\profile.json"
        )
        
        :: Записываем обработанную строку в новый файл
        echo !line!
    )
)

:: Перезаписываем оригинальный файл измененным содержимым
move /y "%temp_file%" "%file_path%" >nul
echo Файл успешно обновлен.
sub_converter.exe