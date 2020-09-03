# Микросервис Sanic-Users
## Настройка программы:
### Установить зависимостей
`pip install -r requirements.txt`
### Создать .env файл в корне с переменными
* `TOKEN_KEY=`ldngffgjkdfdkldjkfdjk
* `DB_HOST=`localhost
* `DB_PORT=`5432
* `DB_DATABASE=`user_offers
* `DB_USER=`username
* `DB_PASSWORD=`password
### Добавить полный путь к src в PYTHONPATH
`export PYTHONPATH='/.../src'`
## Запуск программы:
`python run.py`
## Запуск тестов
`pytest`