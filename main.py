from datetime import datetime
from os import path, remove, getcwd, mkdir
from re import search
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

from easygui import fileopenbox
from pyexiv2 import Image

# Форматы файлов которые будут проверяться на наличие даты съёмки
file_formats = (
    '.jpg', '.jpeg', '.png', '.raw', '.bmp', '.webp',
    '.tiff', '.tif', '.cr2', '.nef', '.arw', '.orf',
    '.rw2', '.pef', '.sr2', '.dng', '.heic', '.heif')

# Подсчёт файлов без даты съёмки для статистики
files_without_date = 0

# Выбор исходного архива через GUI
archive_path = fileopenbox(title="Выберите zip-архив", default="*.zip")
if not archive_path:
    print("Файл не выбран")
    exit()

# Создание папки для сохранения архивов
folder_name = "output"
if not path.exists(folder_name):
    mkdir(folder_name)

# Путь к новому архиву
new_archive_path = f"{folder_name}\\{path.basename(archive_path)}"

print(f"Выбранный файл: {archive_path}")


# Функция для извлечения даты из имени файла
def extract_date_from_filename(filename):
    match = search(r"(\d{4})[-_]?(\d{2})[-_]?(\d{2})[-_]?(\d{2})[-_]?(\d{2})[-_]?(\d{2})", filename)
    if match:
        year, month, day, hour, minute, second = match.groups()
        # print(f"Найдено совпадение для файла '{filename}': {year}-{month}-{day} {hour}:{minute}:{second}")
        try:
            return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        except ValueError as e:
            print(f"Ошибка при преобразовании даты из файла '{filename}': {e}")
            return None
    return None


# Работа с файлами внутри архива
with ZipFile(archive_path, 'r') as archive:
    with ZipFile(new_archive_path, 'w') as new_archive:
        for file_info in archive.infolist():
            file_name = file_info.filename
            if file_name.endswith(file_formats):
                with archive.open(file_info) as file:
                    file_data = file.read()

                    date_from_filename = extract_date_from_filename(file_name)

                    if date_from_filename:
                        # Создаем временный файл для работы с pyexiv2
                        with NamedTemporaryFile(delete=False) as temp_file:
                            temp_file.write(file_data)
                            temp_file_path = temp_file.name

                        try:
                            with Image(temp_file_path) as img:
                                metadata = img.read_exif()

                                if 'Exif.Photo.DateTimeOriginal' not in metadata:
                                    formatted_date = date_from_filename.strftime('%Y:%m:%d %H:%M:%S')
                                    print(f"Установлена дата съёмки для '{file_name}': {formatted_date}")
                                    metadata.update({
                                        'Exif.Photo.DateTimeOriginal': formatted_date,
                                        'Exif.Image.DateTime': formatted_date,
                                        'Exif.Photo.DateTimeDigitized': formatted_date
                                    })
                                    files_without_date += 1
                                img.modify_exif(metadata)  # Сохраняем обновленные метаданные

                            with open(temp_file_path, 'rb') as updated_file:
                                updated_file_data = updated_file.read()

                            new_archive.writestr(file_info, updated_file_data)

                        finally:
                            remove(temp_file_path)
                    else:
                        new_archive.writestr(file_info, file_data)  # Добавляем файл в архив без изменений
            else:
                new_archive.writestr(file_info, archive.read(file_info))  # Копируем остальные файлы без изменений

print()
print(f"Изначальное количество файлов без даты съёмки: {files_without_date}")
print(f"Изменённый архив находится в {getcwd()}\\{new_archive_path}")