from peewee_async import PostgresqlDatabase


DB_HOST = 'localhost'
DB_DATABASE = 'user_offers'
DB_PORT = '5432'
DB_USER = 'username'
DB_PASSWORD = 'password'
DB_URL = f'{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'

db = PostgresqlDatabase(
    DB_DATABASE,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
)
