<h1 align=center>🌟Проект YaMDB🌟</h1>

## 📄 **Описание**

Данный проект направлен на сбор пользовательских рейтингов произведений,
таких как фильмы, книги, музыка и т.д.

Пользователи могут добовлять произведения, оставлять отзывы и комментарии к ним.

<br>
<br>

## 🛠️ Инструкция по установке

Клонируем проект:
```
git clone git@github.com:vglazasmotri/api_yamdb.git
```

Переходим в папку с проектом:
```
cd api_yamdb
```

Eстанавливаем виртуальное окружение:

```
python -m venv venv
```

Активируем виртуальное окружение:
```
source venv/Scripts/activate
```

Обновляем Pip:
```
python -m pip install --upgrade pip
```
Устанавливаем зависимости:
```
pip install -r requirements.txt
```

Выполняем миграции:
```
python yatube/manage.py makemigrations
```
```
python yatube/manage.py migrate
```

Создаем суперпользователя:
```
python yatube/manage.py createsuperuser
```

Можно запускать проект:
```
python manage.py runserver
```

<br>
<br>

## 🎞️ Примеры

Для регистрации нужно отправить запрос на `https://<Домен_сайта>/api/v1/auth/signup/`

```json
{
  "email": "user@example.com",
  "username": "string"
}
```

Для получения токена нужно отправить запрос на `https://<Домен_сайта>/api/v1/auth/token/`

```json
{
  "username": "string",
  "confirmation_code": "string"
}
```

Больше примеров можно найти в [документации](https://<Домен_сайта>/redoc/) проекта.


## 🛠️ Применяемые технологии:
- Python 3.7
- Django 3.2
- Django Rest Framework 3.12.4
- Simplejwt 4.7.1


## 💪💪💪 Авторы:

- Владислав Коновалов 
(https://github.com/idnnowi "Владислав Коновалов (Python-разработчик + Ревью)")
  -- категории (Categories), жанры (Genres) и произведения (Titles): модели,
  представления и эндпойнты для них.

- Артур Безроков 
(https://github.com/Archea888 "Артур Безроков (Python-разработчик)")
  -- отзывы (Review) и комментарии (Comments): модели,
представления, эндпойнты для них, рейтинги произведений;

- Сергей Сыч 
(https://github.com/vglazasmotri "Сергей Сыч (Python-разработчик + Тимлид)")
  -- система управления пользователями (Auth и Users):
  система регистрации и аутентификации, права доступа, работа с токеном,
  система подтверждения через e-mail;
