#  Получаем образ Python с платформы Docker
FROM python:3.11.5-alpine

# Задаем рабочий директорий
WORKDIR /opt/app

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем файл для запуска бота
COPY . .

# Запускаем приложение
CMD python devman.py
