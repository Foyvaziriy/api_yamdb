# API YaMDb
## Описание

**YaMDb** - это сервис, на котором пользователи могут писать рецензии на произведения, такие как книги, фильмы, музыка и т.д.. Каждая рецензия открывает отдельный тред, в котором авторизованные пользователи могут оставлять комментарии и дискутировать.

Произведения делятся на категории, и в каждой категории есть определенные жанры. Например: Достоевский "Преступление и наказание" - это произведение в категории *книги*, а жанр - *роман*.

При написании рецензии пользователь выставляяет оценку по десятибальной шкале, на основе этих оценок у произведения формирутся рейтинг.  

## Стек технологий
- Django
- Django REST Framework
- DRF Simple JWT
- SQLite

## Авторы:

- Эмилар Локтев (@itsme_emichka)
- Никита Соловьев (@Nikita_Solovev_V)
- Евгений Обгольц (@eobgolts)

## Как запустить проект
1. **Клонировать репозиторий**  
`git clone https://github.com/itsme-emichka/api_yamdb.git`

2. **Перейти в директорию проекта**  
`cd api_yamdb`

3. **Создать файл** `.env` **со следующими переменными**
    - SECRET_KEY
    - DEBUG

4. **Создать и активировать виртуальное окружение**  
    - `python -m venv venv`
    - Windows - `source venv/Scripts/activate`  
       Linux/MacOS - `source venv/bin/activate`

5. **Поставить зависимости**  
`pip install -r requirements.txt`

6. **Перейти в директорию с файлом** `manage.py`  
`cd api_yamdb`

7. **Применить миграции**  
`python manage.py migrate`

8. **Запустить сервер**  
`python manage.py runserver`

## Примеры запросов к API
>Полная спецификация API доступна по адресу http://your_domain/redoc  
>Для тестирования API можете использовать postman-collection  

**GET** `http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/`  
**Response:**  
```
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "text": "string",
            "author": "string",
            "score": 1,
            "pub_date": "2019-08-24T14:15:22Z"
        }
    ]
}
```
___
**GET** `http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/`  
**Response:**
```
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "text": "string",
            "author": "string",
            "pub_date": "2019-08-24T14:15:22Z"
        }
    ]
}
```
___
**POST** `http://127.0.0.1:8000/api/v1/titles/`  
```
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```
**Response:**  
```
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
        {
            "name": "string",
            "slug": "string"
        }
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}
```
___
**GET** `http://127.0.0.1:8000/api/v1/titles/`  
**Response:**  
```
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
            {
                "name": "string",
                "slug": "string"
            }
        ],
        "category": {
                "name": "string",
                "slug": "string"
            }
        }
    ]
}
```