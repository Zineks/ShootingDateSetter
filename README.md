# ShootingDateSetter
> Установка даты съёмки фото на основе названия файла

Скрипт позволяет установить дату съёмки для каждого фото в выбранном zip-архиве. Дата определяется по названию файла с помощью регулярных выражений. 

Сейчас обрабатываются даты формата `YYYY-MM-DD_HH-MM-SS`, `YYYYMMDDHHMMSS`, `YYYY_MM_DD-HH_MM_SS` и другие подобные типы.

## Как использовать
#### Установка
Перед дальнейшей установкой вы должны установить Python (желательно 3.11 и выше). Скачать его можно на [здесь](https://www.python.org/).

Клонируйте репозиторий:
```
git clone https://github.com/Zineks/ShootingDateSetter
cd ./ShootingDateSetter
```
Запустите `install.bat` или настройте окружение с зависимостями вручную:
```
python -m venv ./venv
pip install -r requirements.txt
```
#### Запуск
Запустите `run.bat` или активируйте окружение вручную:
```
.\venv\Scripts\Activate
python main.py
```
> Примечание: для Unix систем используйте ```.\venv\Scripts\Activate```
#### Работа программы
При запуске вы увидите диалоговое окно в котором необходимо выбрать нужный вам zip-архив с фотографиями. После выбора подождите пока программа завершит работу, новый архив с добавленными датами будет создан в папке (по умолчанию) ```./output```
##### Видео демонстрация
https://github.com/user-attachments/assets/8d03a6ab-bcf7-46f1-828d-d56572880924
