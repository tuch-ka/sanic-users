from typing import Optional
import bcrypt

import peewee
from peewee import IntegrityError

from . import BasicModel
from database import manager

from auth import create_token


class User(BasicModel):

    __token = None

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
    async def create(cls, data: dict) -> Optional['User']:
        data['password'] = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        try:
            return await manager.create(cls, **data)
        except IntegrityError:
            return None

    @classmethod
    async def get_by_id(cls, user_id: int) -> Optional['User']:
        try:
            return await manager.get(cls, user_id=user_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    async def auth(cls, data: dict) -> Optional['User']:
        username = data.get('username')
        password = data.get('password')

        try:
            user = await manager.get(cls, username=username)
        except cls.DoesNotExist:
            return None

        if bcrypt.checkpw(password.encode(), user.password.encode()):
            return user
        return None

    @property
    def token(self) -> str:
        if self.__token is None:
            payload = {
                'user_id': self.user_id
            }
            self.__token = create_token(payload=payload)
        return self.__token
