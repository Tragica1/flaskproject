# Выкачиваем из dockerhub образ с python версии 3.9
FROM python:3.10.2
# Устанавливаем рабочую директорию для проекта в контейнере
WORKDIR /flaskProject
# Скачиваем/обновляем необходимые библиотеки для проекта
COPY ../requirements.txt /flaskProject

RUN pip install --upgrade pip -r requirements.txt

COPY . /flaskProject

CMD [ "python", "./app.py" ]
# Устанавливаем порт, который будет использоваться для сервера
EXPOSE 5000

# Запуск docker-compose up