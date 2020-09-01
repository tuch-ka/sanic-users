import peewee
from . import BasicModel
from database import manager


class User(BasicModel):
    user_id = peewee.AutoField()
    username = peewee.CharField(unique=True)
    password = peewee.CharField()
    email = peewee.CharField(null=True)

    def __repr__(self):
        return f'User: {self.username}'

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email
        }

    @classmethod
    async def create(cls, data: dict) -> 'User':
        return await manager.create(cls, **data)

    @classmethod
    async def get_by_id(cls, user_id: int) -> 'User':
        return await manager.get(cls, user_id=user_id)
