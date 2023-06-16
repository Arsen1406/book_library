# book_library

Проект будет доступен по адресу http://127.0.0.1:8000/
Или http://0.0.0.0:8000/


Проект BookLibrary это 📚книжная библиотека, где можно взять почитать разные произведения.

У произведений есть следующие связанные элементы:
- Категории
- Остатки на полке(при взятии автоматом уменьшается, при возврате наоборот)
- Авторы
- Сколько раз их взяли почитать

## Краткое описание функционала
- Книги, Категории, Авторы может добавлять только Администратор.
- Сколько раз книга прочитана высчитывается автоматически. 
- Произведения выдаются на две недели.
- Если спустя две недели не вернуть книги, на email прилетит уведомление, которое напомнит об аренде.
- Читатели могут брать и возвращать книги.
- Читатели могут регистрироваться, и изменять информацию о своем профиле
- Читатели видят только свои заказы
- Читатели видят книги, но не могут их добавлять, удалять и менять

## Технологии
- python 3.7
- django 2.2.16
- django_rest_framework 3.14.0
- celery 5.2.7
- redis 4.5.5
- PyJWT 2.7.0

#.env файл
В ./book_library/ проекта необходимо создать .env файл.
Разместите в нем следующие переменные:

- DB_ENGINE=django.db.backends.postgresql
- DB_NAME=<Имя базы данных>
- POSTGRES_USER=<Имя базы пользователя>
- POSTGRES_PASSWORD=<Пароль базы данных>
- DB_HOST=db
- DB_PORT=<Порт базы данных>
- SECRET_KEY=<Секретный ключ Django>
- CELERY_BROKER=redis://redis:6379/0

## Чтобы развернуть проект
Клонировать репозиторий
```sh
git clone <ssh ссылка>
```
В дирректории проекта выполните комманду, для запуска контейнера
```sh
sudo docker compose up --build -d
```
Выполните миграции
```
sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate
```
Затем необходимо создать superuser 
```sh
sudo docker-compose exec web python manage.py createsuperuser
```
Перейти по адресу сервера
```sh
http://127.0.0.1:8000/
http://0.0.0.0:8000/
```

## Создание книг:
/api/v1/books/ администратор отправляет POST запрос для создания книги.
Читатели могут только смотреть
Поля, которые есть у книг:
- title(Название книги - Обязательное поле)
- description(Описание книги)
- author(Авторов может быть несколько)
- genre(Жанров может быть несколько)
- views(Автоматически увеличивается с каждым взятием на прочтение)
- date_create(Дата добавления книги)
- При GET запросе вернется список книг, с колличеством остатков. 
- Так же будет поле, в наличии книга, или нет.

## Загрузка книг из файла CSV
- /api/v1/upload-books/ На данный адрес необходимо передать файл csv POST запросом
- Поля, которые должны быть в файле:
- Загрузка происходит в фоновом режиме
```
- title <Название книги - str>
- genre <Жанр - str>
- author <Автор книги - str>
- remains <Сколько книг добавить в библиотеку>
```
- Если автора, или жанра нет в бд, они создадутся
- Если Книга есть в бд, она обновится
- Количество книг не обновляется, а добавляется к существующему


## Создание жанров:
/api/v1/genre/ администратор отправляет POST запрос для создания жанра.
Читатели могут только смотреть
Поля, которые есть у жанров:
- title(Название жанра - Обязательное поле)
- description(Описание книги)
- При GET запросе вернется список жанров. 

## Создание авторов:
/api/v1/authors/ администратор отправляет POST запрос для создания автора.
Читатели могут только смотреть
Поля, которые есть у авторов:
- first_name(Имя автора)
- last_name(Фамилия автора)
- birth_day(Дата рождения автора)
- При GET запросе вернется список авторов. 

## Регистрация пользователя:
1. /api/v1/auth/signup/ пользователь отправляет POST запрос с параметрами 
email и username и password для регистрации - обязательные поля. Так же есть first_name и last_name.
2. /api/v1/auth/token/ пользователь отправляет POST-запрос с параметрами 
username и password на эндпоинт. В ответ ему приходит token (JWT-токен).
3. /api/v1/users/me/ по данному энтпоинту пользователь может отправить PATCH
запрос и заполнить поля в своём профайле, или Get запросом просмотреть информацию о себе

## Аренда книг:
/api/v1/rentals/ отправив POST запрос читатель может взять одну, или несколько книг на прочтение.
Поля, которые есть у заказов:
- books(Книги)
- reader(Читатель)
- create_date(Дата аренды)
- return_date(Дата ворврата)

- Для того, чтобы взять книги, необходимо передать `{"books": ["один, или несколько id книги типа INTEGER"]}`
- При GET запросе вернутся только заказы данного читателя
- Чтобы вернуть книги, необходимо передать на /api/v1/rentals/{id заказа}/ DELETE запрос
Книги вернутся на свои полки


## Напоминания о возврате:
- Каждый день Celery запускает таску в 1 час ночи. В ней достаются заказы, у которых истек срок аренды.
- По таким заказам идет рассылка писем на электронную почту.

## Автор Григорян Арсен
