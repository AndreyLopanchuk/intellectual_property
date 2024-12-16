# API для управления библиотекой

## Архитектура приложения

Приложение состоит из следующих слоев:

- API Интерфейс: предоставляет RESTful API для взаимодействия с приложением.
- Сервисный слой: реализует бизнес-логику приложения и взаимодействует с репозиторием для доступа к данным.
- Репозиторий: обеспечивает доступ к данным в базе данных и реализует CRUD (Create, Read, Update, Delete) операции.
- База данных: хранит данные приложения и обеспечивает их сохранность.

#### Контейнеризация

Приложение и БД запускаются в разных Docker контейнерах
Тесты и Тестовая база данных так же запускаются в разных Docker контейнерах

## Установка и Запуск
склонируте репозиторий:
```sh
git clone https://github.com/AndreyLopanchuk/intellectual_property.git
```

Для запуска веб-приложения введите команду:
```sh
docker-compose up --build
```

Запуск с выводом логов тестов при запуске приложения
```sh
docker-compose up --build -d && docker-compose logs -f testapp
```

## Тестирование
 
Повторное тестирование
```sh
docker exec -it testapp  pytest -vv tests/
```  

## Документация

Реализована встроенная FastAP OpenAPI документация.

#### ссылка на задание:  
https://docs.google.com/document/d/17qE_QawFOssdRIaEBzTaN8N-SYmkhh7tdNOy3ZTwHz8/edit?tab=t.0

## Технологический стек
- `PostgreSql` - база данных
- `Fastapi` - фреймворк для разработки RESTful API
- `Uvicorn` - сервер для запуска FastAPI-приложения
- `Pydantic` - библиотека для работы с данными и валидации
- `Sqlalchemy` - библиотека для работы с базой данных
- `Pytest` - фреймворк для написания и запуска тестов
- `Docker` - контейнеризация приложения, БД и тестов
