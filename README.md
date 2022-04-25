# Kvartirka Comments
Api на django по тестовому заданию.

## Задание
Реализовать REST API для системы комментариев блога

## Запуск проекта
1. Скачайте или склонируйте проект.
2. Установите библиотеки из _requirements.txt_
3. Запустите postgres _(я использовал: psql (PostgreSQL) 12.10 (Ubuntu 12.10-0ubuntu0.20.04.1)
)_
   1. Создайте пользователя и БД. Если используете свои имена, их нужно поправить в _settings.py_
   2. Если не знакомы с psql. После установки в терминале введите команды:
   `sudo -u postgres psql postgres`
   3. Введите пароль
   4. В консоли postgres введите команды, _не забудьте про точку с запятой в конце строки_:
   ```
   create user kvartirka with password 'password';
   alter role kvartirka set client_encoding to 'utf8';
   create database kvartirka_comments_db owner kvartirka;
   ```
   5. Выходим из консоли postgres `\q`
4. Дальше всё как обычно:
   1. делаем миграцию `./manage.py migrate`,
   2. создаем суперпользователя `./manage.py createsuperuser`
   3. запускаем сервер `./manage runserver`.

## Работа с API

