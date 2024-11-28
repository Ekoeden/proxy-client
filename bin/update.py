import os
import requests
import zipfile
import shutil

# URL репозитория (замените на ваш)
REPO_URL = "https://github.com/Ekoeden/proxy-client"
ZIP_URL = f"{REPO_URL}/archive/refs/heads/main.zip"
USERDATA_FILE = "userdata.txt" # Локальный файл с версией и пользовательскими данными
DOWNLOAD_PATH = "update.zip" # Путь для загрузки архива
LARGE_FILE = "sing-box.zip" # Заархивированный файл 
EXCLUDE_FILES = ["bin/configs/profile.json", "bin/configs/routes.json", "bin/profile.cmd"]  # Исключения при обновлении

def get_current_version():
    """Чтение текущей версии из файла userdata."""
    if os.path.exists(USERDATA_FILE):
        with open(USERDATA_FILE, "r") as file:
            # Предполагаем, что версия указана на первой строке
            return file.readline().strip()
    return "0.0.0"

def get_latest_version():
    """Получение последней версии из GitHub."""
    response = requests.get(f"{REPO_URL}/raw/main/bin/userdata.txt")
    if response.status_code == 200:
        # Предполагаем, что версия указана на первой строке
        return response.text.splitlines()[0].strip()
    raise Exception("Не удалось получить версию с GitHub.")

def download_update():
    """Скачивание ZIP-архива с обновлениями."""
    print("Скачивание обновлений...")
    response = requests.get(ZIP_URL, stream=True)
    with open(DOWNLOAD_PATH, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
    print("Скачивание завершено.")

def extract_repository():
    """Распаковка содержимого архива репозитория в корневую папку с исключениями."""
    print("Распаковка репозитория...")
    with zipfile.ZipFile(DOWNLOAD_PATH, "r") as zip_ref:
        archive_files = zip_ref.namelist()
        root_folder = next((name for name in archive_files if name.endswith('/')), None)

        if not root_folder:
            raise Exception("Не удалось найти корневую папку в архиве.")

        for file in archive_files:
            if file.startswith(root_folder):
                # Удаляем имя корневой папки архива
                relative_path = file[len(root_folder):]
                if any(relative_path.startswith(exclude) for exclude in EXCLUDE_FILES):
                    print(f"Пропуск файла или папки: {relative_path}")
                    continue

                # Извлечение в папку уровнем выше
                destination_path = os.path.join("..", relative_path)  # ".." для выхода на уровень выше
                if file.endswith('/'):
                    os.makedirs(destination_path, exist_ok=True)
                else:
                    extracted_path = zip_ref.extract(file, ".")  # Временное извлечение
                    destination_full_path = os.path.abspath(destination_path)
                    os.makedirs(os.path.dirname(destination_full_path), exist_ok=True)
                    try:
                        os.rename(extracted_path, destination_path)
                    except FileExistsError:
                        os.remove(destination_path)
                        os.rename(extracted_path, destination_path)

    # Удаление оставшейся root_folder
    abs_root_folder = os.path.abspath(root_folder)
    if os.path.exists(abs_root_folder) and os.path.isdir(abs_root_folder):
        shutil.rmtree(abs_root_folder)

    os.remove(DOWNLOAD_PATH)
    print("Репозиторий распакован.")

def extract_large_file():
    """Распаковка большого файла (sing-box.zip)."""
    print("Распаковка большого файла...")
    if os.path.exists(LARGE_FILE):
        with zipfile.ZipFile(LARGE_FILE, "r") as zip_ref:
            zip_ref.extractall()
        os.remove(LARGE_FILE)
        print("Распаковка завершена.")
    else:
        print(f"Файл {LARGE_FILE} не найден.")

def main():
    try:
        current_version = get_current_version()
        latest_version = get_latest_version()
        print(f"Текущая версия: {current_version}")
        print(f"Последняя версия: {latest_version}")

        if current_version != latest_version:
            print("Доступно обновление! Начинаем загрузку...")
            download_update()
            extract_repository()

            print("Обновление больших файлов...")
            extract_large_file()

            # Обновляем файл userdata
            with open(USERDATA_FILE, "w") as file:
                file.write(latest_version + "\n")
                file.write("Additional user data here...")
            print("Приложение обновлено до версии", latest_version)
        else:
            print("Вы используете последнюю версию.")
    except Exception as e:
        print("Ошибка обновления:", e)

if __name__ == "__main__":
    main()
