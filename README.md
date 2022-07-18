![example workflow](https://github.com/irinaexzellent/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# О ПРОЕКТЕ

Проект yamdb_final создан для демонстрации методики увеличения скорости, качества и безопасности разработки DevOps (Development Operations) и идеи Continuous Integration (CI),
суть которых заключается в интеграции и автоматизации следующих процессов:
* синхронизация изменений в коде
* сборка, запуск и тестирование приложения в среде, аналогичной среде боевого сервера
* деплой на сервер после успешного прохождения всех тестов
* уведомление об успешном прохождении всех этапов

Приложение взято из проекта https://github.com/irinaexzellent/api_yamdb, который представляет собой API сервиса отзывов о фильмах, книгах и музыке.
Зарегистрированные пользователи могут оставлять отзывы (Review) на произведения (Title).
Произведения делятся на категории (Category): «Книги», «Фильмы», «Музыка». 
Список категорий может быть расширен администратором. Приложение сделано с помощью Django REST Framework.

Для Continuous Integration в проекте используется облачный сервис GitHub Actions.
Для него описана последовательность команд (workflow), которая будет выполняться после события push в репозиторий.

# ОПИСАНИЕ КОМАНД ДЛЯ ЗАПУСКА ПРИЛОЖЕНИЯ

1. Клонировать проект:
```
git clone https://github.com/irinaexzellent/yamdb_final
```
2. Добавить **Action secrets** в репозитории на GitHub в разделе settings -> Secrets:

```
DOCKER_PASSWORD - пароль от DockerHub;
DOCKER_USERNAME - имя пользователя на DockerHub;
HOST - ip-адрес сервера;
SSH_KEY - приватный ssh ключ (публичный должен быть на сервере);
TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=new_user(установить свой)
POSTGRES_PASSWORD=new_password(установить свой)
DB_HOST=postgres
DB_PORT=5432
```
3. Установить соединение с сервером по протоколу ssh:
```
ssh username@server_address
```
username - имя пользователя, под которым будет выполнено подключение к серверу,
    
server_address - IP-адрес сервера или доменное имя.
```
*  Добавить файлы docker-compose.yaml и nginx/default.conf из проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно
```
# Проверка работы приложения

Внести любые изменения в проект и выполнить:
```
git add .
git commit -m "..."
git push
```
Комманда git push является триггером workflow проекта.
При выполнении команды git push запустится набор блоков комманд jobs (см. файл yamdb_workflow.yaml).
Последовательно будут выполнены следующие этапы:
* tests - тестирование проекта на соответствие PEP8 и тестам pytest.
* build_and_push_to_docker_hub - после успешного прохождения тестов собирается образ (image) для docker контейнера 
и отправлятеся в DockerHub
* deploy - после отправки образа на DockerHub начинается деплой проекта на сервере.
* send_message - после сборки и запуска контейнеров происходит отправка сообщения в 
  телеграм об успешном окончании workflow

После выполнения вышеуказанных процедур необходимо установить соединение с сервером:
```
ssh username@server_address
```
Отобразить список работающих контейнеров:
```
sudo docker container ls
```
Статус контейнеров будет в состоянии Up:
```
CONTAINER ID   IMAGE                             COMMAND                  CREATED          STATUS          PORTS                               NAMES
0e71c6c6234c   nginx:1.21.3-alpine               "/docker-entrypoint.…"   39 minutes ago   Up 39 minutes   0.0.0.0:80->80/tcp, :::80->80/tcp   irina-nginx-1
616ca90cb80a   irinaexcellent/api_yamdb:latest   "gunicorn api_yamdb.…"   39 minutes ago   Up 39 minutes                                       irina-web-1
5e0bbb3354ee   postgres:13.0-alpine              "docker-entrypoint.s…"   39 minutes ago   Up 39 minutes   5432/tcp                            irina-db-1
```
Выполнить миграции в контейнере web:
```
sudo docker compose exec web python manage.py migrate
```

Наполнить базу данных начальными тестовыми данными:
```
sudo docker compose exec web python manage.py > dump.json
```

Для создания нового суперпользователя можно выполнить команду:
```
sudo docker compose exec web python manage.py createsuperuser
```
и далее указать: 
```
Email:
Username:
Password:
Password (again):
```
Для обращения к API проекта:

* http://158.160.2.160/api/v1/auth/token/
* http://158.160.2.160/api/v1/users/
* http://158.160.2.160/api/v1/categories/
* http://158.160.2.160/api/v1/genres/
* http://158.160.2.160/api/v1/titles/
* http://158.160.2.160/api/v1/titles/{title_id}/reviews/
* http://158.160.2.160/api/v1/titles/{title_id}/reviews/{review_id}/
* http://158.160.2.160/api/v1/titles/{title_id}/reviews/{review_id}/comments/

Cписок и подробное описание доступных запросов к приложению можно посмотреть:
* http://158.160.2.160/redoc/

Для остановки и удаления контейнеров и образов на сервере:
```
sudo docker stop $(sudo docker ps -a -q) && sudo docker rm $(sudo docker ps -a -q) && sudo docker rmi $(sudo docker images -q)
```
Для удаления volume базы данных:
```
sudo docker volume rm yamdb_final_postgres_data
```

## Автор

* **Ирина Иконникова** - (https://github.com/irinaexzellent)


