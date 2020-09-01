from sanic import Blueprint
from sanic.response import json

from marshmallow import ValidationError
from schemas.user import UserRegistrySchema

from models.user import User

from peewee import IntegrityError


bp = Blueprint('user')


@bp.post('/registry')
async def create_user(request):
    """Создаёт пользователя в бд"""
    try:
        user_data = UserRegistrySchema().load(request.json)
    except ValidationError as error:
        return json(error.messages, status=400)

    try:
        user = await User.create(data=user_data)
    except IntegrityError as error:
        return json(error.args, 400)

    return json(user.to_dict(), status=201)


@bp.get('/<user_id:int>')
async def read_user(request, user_id):
    """Считывает данные пользователя из бд"""
    return json(
        {
            'user_id': user_id,
        },
        status=200
    )
