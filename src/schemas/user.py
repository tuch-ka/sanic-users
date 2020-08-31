from marshmallow import fields

from . import BasicSchema


class UserRegistrySchema(BasicSchema):
    """Валидирование входных данных при создании пользователя"""
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=False)


class UserAuthSchema(BasicSchema):
    """Валидирование входных данных при авторизации пользователя"""
    username = fields.Str(required=True)
    password = fields.Str(required=True)
