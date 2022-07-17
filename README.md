[![yamdb_final workflow](https://github.com/irinaexcellent/yamdb_final/workflows/yamdb_final%20workflow/badge.svg)](https://github.com/irinaexcellent/yamdb_final/actions?query=workflow%3A%22yamdb_final+workflow%22)
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

2. Добавить файл .env с настройками базы данных на сервер:

* Установить соединение с сервером по протоколу ssh:
    ```
    ssh username@server_address
    ```
    username - имя пользователя, под которым будет выполнено подключение к серверу,
    
    server_address - IP-адрес сервера или доменное имя.
    ```
* В домашней директории проекта
    Создать папку **new_directory/**:
    ```
    mkdir new_directory
    ```
    В папке **new_directory** создать папку **yamdb_final/**:
    ```
    mkdir new_directory/yamdb_final
    ```
    В папке **yamdb_final** создать файл **.env**:
    ```
    touch www/yamdb_final/.env
    ```

* Добавить настройки в файл **.env**:
    ```
    sudo nano new_directory/yamdb_final/.env
    ```
    Пример добавляемых настроек:
    ```
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=new_user
    POSTGRES_PASSWORD=new_password
    DB_HOST=postgres
    DB_PORT=5432
    ```

* Добавить Action secrets в репозитории на GitHub в разделе settings -> Secrets:

```
DOCKER_PASSWORD - пароль от DockerHub;
DOCKER_USERNAME - имя пользователя на DockerHub;
HOST - ip-адрес сервера;
SSH_KEY - приватный ssh ключ (публичный должен быть на сервере);
TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)
```
*  Добавить файлы docker-compose.yaml и nginx/default.conf из проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно

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
В списке контейнеров копировать CONTAINER ID контейнера username/yamdb_final_web:latest (username - имя пользователя на DockerHub):
```
CONTAINER ID   IMAGE                            COMMAND                  CREATED          STATUS          PORTS                NAMES
0361a982109d   nginx:1.19.6                     "/docker-entrypoint.…"   50 minutes ago   Up 50 minutes   0.0.0.0:80->80/tcp   yamdb_final_nginx_1
a47ce31d4b7b   username/yamdb_final_web:latest  "/bin/sh -c 'gunicor…"   50 minutes ago   Up 50 minutes                        yamdb_final_web_1
aed19f6751f3   postgres:13.1                    "docker-entrypoint.s…"   50 minutes ago   Up 50 minutes   5432/tcp             yamdb_final_postgres_1
```
Выполнить вход в контейнер:
```
sudo docker exec -it a47ce31d4b7b bash
```
Выполнить миграции внутри контейнера:
```
python manage.py migrate
```
Наполнить базу данных начальными тестовыми данными:
```
python3 manage.py shell
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()
python manage.py loaddata dump.json
```

Для создания нового суперпользователя можно выполнить команду:
```
$ python manage.py createsuperuser
```
и далее указать: 
```
Email:
Username:
Password:
Password (again):
```
Для обращения к API проекта:

* http://IP-сервера/api/v1/auth/token/
* http://IP-сервера/api/v1/users/
* http://IP-сервера/api/v1/categories/
* http://IP-сервера/api/v1/genres/
* http://IP-сервера/api/v1/titles/
* http://IP-сервера/api/v1/titles/{title_id}/reviews/
* http://IP-сервера/api/v1/titles/{title_id}/reviews/{review_id}/
* http://IP-сервера/api/v1/titles/{title_id}/reviews/{review_id}/comments/

Cписок и подробное описание доступных запросов к приложению можно посмотреть:
* http://IP-сервера/redoc/

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


