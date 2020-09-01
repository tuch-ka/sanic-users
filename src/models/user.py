import peewee
from . import BasicModel


class User(BasicModel):
    username = peewee.CharField(unique=True)
    password = peewee.CharField()
    email = peewee.CharField()

    def __repr__(self):
        return f'User: {self.username}'
