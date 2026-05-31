# Laboratory work VIII: Docker

## Author
Павел Дацковских 
GitHub: PavelDats1
Группа: ИУ8-21

## Цель работы
Изучение системы автоматизации развёртывания и управления приложениями на примере **Docker**.

## Выполнение

### 1. Установка Docker
Docker был установлен на систему Ubuntu 24.04.  
```bash
$ docker --version
Docker version 29.5.2, build 79eb04c
```
###2. Создание файлов проекта
## 2.1. main.py — веб-приложение на Flask с подключением к MariaDB
```bash
from flask import Flask, request, render_template_string
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('DB_USER', 'user'),
        password=os.environ.get('DB_PASSWORD', 'password'),
        database=os.environ.get('DB_NAME', 'messages_db')
    )
```
## 2.2. requirements.txt — зависимости Python
```bash
Flask==2.3.3
mysql-connector-python==8.1.0
```

## 2.3. Dockerfile — инструкция для сборки образа
```bash
FROM python:3.9-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
EXPOSE 5000
CMD ["python", "main.py"]
```
## 2.4. docker-compose.yml — описание двух сервисов
```bash
services:
  db:
    image: mariadb:10.6
    container_name: lab08_db
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: messages_db
      MYSQL_USER: user
      MYSQL_PASSWORD: password
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql

  web:
    build: .
    container_name: lab08_web
    environment:
      DB_HOST: db
      DB_USER: user
      DB_PASSWORD: password
      DB_NAME: messages_db
    ports:
      - "5000:5000"
    depends_on:
      - db

volumes:
  db_data:
```
### 3. Сборка и запуск
```bash
$ docker compose build --no-cache
$ docker compose up -d
```
