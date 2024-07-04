# It-solution test task

## Описание 

Для приложения используются библиотеки __fastapi__ __sqlalchemy__ __asyncio__ и __aiohttp__ 



## Установки

Для поднятия проекта с помощью docker:

    Открыть cmd из папки itsolut-test-task
    Ввести docker-compose up

Для поднятия вне docker:
    
    Создать .env по аналогии с .env.template 
    Ввести полный путь в переменную DB_PATH 

    Создать окружение python -m venv .venv 
    Установить зависимости pip install ./app/requirements.txt
    Перейти в папку с приложением cd ./app
    
    Применить миграции моделей в БД alembic upgrade head

    Ввести в терминал uvicorn main:app 

## Приложение 

Реализована базовая аутентификация - для входа использовать __admin:admin__

Путь __/api/get_adverts/__ парсит сайт farpost.ru и достает оттуда первые 10 объявлений, после чего сохраняет их в бд

Путь __/api/get_advert/{id}__ выводит элемент из бд по id

Путь __/api/get_farpost_advert/{farpost_id}__ выводит элемент из бд по ключу farpost_id 

