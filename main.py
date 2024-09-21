import os
import re
import tempfile
import zipfile
from datetime import datetime
from tkinter.filedialog import askopenfilename

from pyexiv2 import Image

files_without_date = 0

archive_path = askopenfilename()
new_archive_path = f"output\\{os.path.basename(archive_path)}"

print(f"Выбранный файл: {archive_path}")


# Функция для извлечения даты из имени файла
def extract_date_from_filename(filename):
    match = re.search(r"(\d{4})[-_]?(\d{2})[-_]?(\d{2})[-_]?(\d{2})[-_]?(\d{2})[-_]?(\d{2})", filename)
    if match:
        year, month, day, hour, minute, second = match.groups()
        print(
            f"Найдено совпадение для файла '{filename}': {year}-{month}-{day} {hour}:{minute}:{second}")
        try:
            return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        except ValueError as e:
            print(f"Ошибка при преобразовании даты из файла '{filename}': {e}")
            return None
    return None


# Работы с файлами внутри архива
with zipfile.ZipFile(archive_path, 'r') as archive:
    with zipfile.ZipFile(new_archive_path, 'w') as new_archive:
        for file_info in archive.infolist():
            file_name = file_info.filename
            if file_name.endswith(('.jpg', '.jpeg', '.png')):
                with archive.open(file_info) as file:
                    file_data = file.read()

                    date_from_filename = extract_date_from_filename(file_name)

                    if date_from_filename:
                        # Создаем временный файл для работы с pyexiv2
                        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                            temp_file.write(file_data)
                            temp_file_path = temp_file.name

                        try:
                            with Image(temp_file_path) as img:
                                metadata = img.read_exif()

                                if 'Exif.Photo.DateTimeOriginal' not in metadata:
                                    formatted_date = date_from_filename.strftime('%Y:%m:%d %H:%M:%S')
                                    metadata.update({
                                        'Exif.Photo.DateTimeOriginal': formatted_date,
                                        'Exif.Image.DateTime': formatted_date,
                                        'Exif.Photo.DateTimeDigitized': formatted_date
                                    })
                                    files_without_date += 1
                                img.modify_exif(metadata)  # Сохраняем обновленные метаданные

                            with open(temp_file_path, 'rb') as updated_file:
                                updated_file_data = updated_file.read()

                            new_archive.writestr(file_info, updated_file_data)  # Добавляем обновленный файл в новый архив

                        finally:
                            os.remove(temp_file_path)
                    else:
                        new_archive.writestr(file_info, file_data)  # Добавляем файл в архив без изменений
            else:
                new_archive.writestr(file_info, archive.read(file_info))  # Копируем остальные файлы без изменений

print(f"Файлы заархивированы в {os.getcwd()}\\{new_archive_path}")
print(f"Изначальное количество файлов без даты съемки: {files_without_date}")