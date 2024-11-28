import os
import requests
import zipfile
import shutil

# URL репозитория (замените на ваш)
REPO_URL = "https://github.com/Ekoeden/proxy-client"
ZIP_URL = f"{REPO_URL}/archive/refs/heads/main.zip"
SING_BOX_ZIP_PATH = "bin/sing-box.zip"  # Путь к архиву sing-box.zip внутри репозитория
BIN_DIR = "bin"  # Каталог, куда будет распакован sing-box.zip
VERSION_FILE = "version.txt"
DOWNLOAD_PATH = "update.zip"
EXCLUDE_FILES = ["config.json", "user_data/"]  # Список файлов и папок для исключения

def get_current_version():
    """Чтение текущей версии из локального файла."""
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as file:
            return file.read().strip()
    return "0.0.0"

def get_latest_version():
    """Получение последней версии из GitHub."""
    response = requests.get(f"{REPO_URL}/raw/main/{VERSION_FILE}")
    if response.status_code == 200:
        return response.text.strip()
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
    """Распаковка содержимого архива репозитория в текущую папку с исключениями."""
    print("Распаковка репозитория...")
    with zipfile.ZipFile(DOWNLOAD_PATH, "r") as zip_ref:
        # Получаем список всех файлов и директорий в архиве
        archive_files = zip_ref.namelist()

        # Определяем имя корневой папки в архиве (например, proxy-client-main/)
        root_folder = next((name for name in archive_files if name.endswith('/')), None)

        if not root_folder:
            raise Exception("Не удалось найти корневую папку в архиве.")

        # Извлекаем только содержимое корневой папки
        for file in archive_files:
            if file.startswith(root_folder):  # Проверяем, что файл относится к корневой папке
                relative_path = file[len(root_folder):]  # Убираем имя корневой папки из пути

                # Проверяем, входит ли файл в список исключений
                if any(relative_path.startswith(exclude) for exclude in EXCLUDE_FILES):
                    print(f"Пропуск файла или папки: {relative_path}")
                    continue

                destination_path = os.path.join(".", relative_path)

                # Создаем директории, если это папка
                if file.endswith('/'):
                    os.makedirs(destination_path, exist_ok=True)
                else:
                    # Извлекаем файл во временную директорию
                    extracted_path = zip_ref.extract(file, ".")
                    try:
                        # Переименовываем файл
                        os.rename(extracted_path, destination_path)
                    except FileExistsError:
                        # Если файл существует, заменяем его
                        os.remove(destination_path)
                        os.rename(extracted_path, destination_path)

    if os.path.exists(root_folder):
        shutil.rmtree(root_folder)
    os.remove(DOWNLOAD_PATH)
    print("Репозиторий распакован.")

def extract_large_file():
    """Распаковка sing-box.zip в папке bin."""
    print("Распаковка sing-box.zip...")
    zip_file_path = os.path.join(BIN_DIR, "sing-box.zip")
    if not os.path.exists(zip_file_path):
        raise Exception(f"Архив {zip_file_path} не найден.")

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(BIN_DIR)
    os.remove(zip_file_path)  # Удаляем архив после распаковки
    print("Распаковка завершена.")

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
            extract_large_file()

            with open(VERSION_FILE, "w") as file:
                file.write(latest_version)
            print("Приложение обновлено до версии", latest_version)
        else:
            print("Вы используете последнюю версию.")
    except Exception as e:
        print("Ошибка обновления:", e)

if __name__ == "__main__":
    main()
