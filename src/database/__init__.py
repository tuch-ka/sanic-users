from peewee_async import PostgresqlDatabase, Manager
import config


db = PostgresqlDatabase(
    config.DB_DATABASE,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    port=config.DB_PORT,
)

manager = Manager(db)
