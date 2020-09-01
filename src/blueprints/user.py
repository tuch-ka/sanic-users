from sanic import Blueprint
from sanic.response import json, empty

from schemas.user import UserRegistrySchema

from models.user import User
from auth import auth_required

from marshmallow import ValidationError

bp = Blueprint('user')


@bp.post('/registry')
async def create_user(request):
    """Создаёт пользователя в бд"""
    try:
        user_data = UserRegistrySchema().load(request.json)
    except ValidationError as error:
        return json(error.messages, status=400)

    user = await User.create(data=user_data)
    if user is None:
        return empty(409)

    return json(user.to_dict(), status=201)


@bp.get('/<user_id:int>')
@auth_required
async def read_user(request, user_id):
    """Считывает данные пользователя из бд"""

    user = await User.get_by_id(user_id)
    if user is None:
        return empty(404)

    return json(user.to_dict(), status=200)
